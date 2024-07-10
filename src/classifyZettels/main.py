import itertools
from itertools import chain
from pathlib import Path
from sqlite3 import Connection, connect
from typing import Hashable, List, Tuple

import click
import pandas
from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence
from pandas import DataFrame, Series
from progress.bar import Bar
from pyfs import isFile, resolvePath

from src.classifyZettels import NATURE_SUBJECTS


def buildRunnableSequence(
    classifications: chain, model: str = "llama3"
) -> RunnableSequence:

    llm: Ollama = Ollama(model=model)

    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"Only return classifications. Only return one classification. Do not return markdown. Do not include astericks. Classify prompts as one of the following: {' '.join(classifications)}",  # noqa: E501
            ),
            ("user", "{input}"),
        ]
    )

    output: StrOutputParser = StrOutputParser()

    return prompt | llm | output


def readDB(dbPath: Path, conn: Connection) -> DataFrame:
    sqlQuery: str = "SELECT * FROM zettels"
    df: DataFrame = pandas.read_sql_query(sql=sqlQuery, con=conn)
    return df


def inference(
    df: DataFrame, llmRunner: RunnableSequence
) -> List[Tuple[int, str]]:
    data: List[Tuple[int, str]] = []

    with Bar("Inferencing data...", max=df.shape[0]) as bar:
        row: Series
        idx: Hashable
        for idx, row in df.iterrows():
            title: str = row["title"]
            abstract: str = row["summary"]

            prompt: str = f"title: {title} $$$ abstract: {abstract}"

            output: str = llmRunner.invoke(input=prompt)

            data.append((idx, output))

            bar.next()

    return data


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a Zettelgeist database",
)
def main(inputPath: Path) -> None:
    absInputPath: Path = resolvePath(path=inputPath)

    if not isFile(path=absInputPath):
        print(f"{absInputPath} is not a file")
        exit(1)

    conn: Connection = connect(database=absInputPath)
    df: DataFrame = readDB(dbPath=absInputPath, conn=conn)

    topics: chain = itertools.chain.from_iterable(NATURE_SUBJECTS.values())
    # subjects: chain = itertools.chain.from_iterable(NATURE_SUBJECTS.keys())

    llmRunner: RunnableSequence = buildRunnableSequence(classifications=topics)

    data: List[Tuple[int, str]] = inference(df=df, llmRunner=llmRunner)

    datum: Tuple[int, str]
    for datum in data:
        # print(datum[0], datum[1])
        df.at[datum[0], "tags"] = datum[1]

    df.to_sql(name="zettels", con=conn, if_exists="replace", index=False)
    conn.close()


if __name__ == "__main__":
    main()
