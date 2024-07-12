import itertools
from itertools import chain
from pathlib import Path
from sqlite3 import Connection, connect
from string import Template
from subprocess import PIPE, CompletedProcess, Popen  # nosec
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

from src.classifyZettels import NATURE_SUBJECTS, SCOPUS_SUBJECTS


def buildRunnableSequence(
    classifications: chain, ollamaModel: str
) -> RunnableSequence:

    llm: Ollama = Ollama(model=ollamaModel)

    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"Only return classifications. Only return one classification. Do not return markdown. Do not include astericks. Use proper grammar. Classify prompts as one of the following: {' '.join(classifications)}",  # noqa: E501
            ),
            ("user", "{input}"),
        ]
    )

    output: StrOutputParser = StrOutputParser()
    return prompt | llm | output


def readDB(dbPath: Path) -> DataFrame:
    sqlQuery: str = "SELECT title, summary, filename FROM zettels"
    conn: Connection = connect(database=dbPath)
    df: DataFrame = pandas.read_sql_query(sql=sqlQuery, con=conn)
    conn.close()
    return df


def inference(
    df: DataFrame,
    llmRunner: RunnableSequence,
    tagName: str,
    model: str,
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
            data.append((idx, model + "_" + tagName + "_" + output))
            bar.next()

    return data


def writeTagsToFile(data: List[Tuple[int, str]], filepaths: Series) -> None:
    cmdTemplate: Template = Template(
        template='zettel --file ${filepath} --append-tag "${tag}" --in-place',
    )

    with Bar("Writing tags to files...", max=filepaths.size) as bar:
        datum: Tuple[int, str]
        for datum in data:
            fp: str = filepaths[datum[0]]

            cmd: str = cmdTemplate.substitute(filepath=fp, tag=datum[1])

            process: CompletedProcess = Popen(
                cmd,
                shell=True,
                stdout=PIPE,
            )  # nosec

            if process.returncode is not None:
                print(fp)

            bar.next()


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a Zettelgeist database",
)
@click.option(
    "-c",
    "--classes",
    "classificationName",
    type=click.Choice(
        [
            "nature-subjects",
            "nature-topics",
            "scopus-subjects",
            "scopus-topics",
        ]
    ),
    required=True,
    help="Classifications to use",
)
@click.option(
    "-m",
    "--model",
    "model",
    type=str,
    required=True,
    help="A valid Ollama model to utilize as a classifier",
)
def main(inputPath: Path, classificationName: str, model: str) -> None:
    absInputPath: Path = resolvePath(path=inputPath)

    if not isFile(path=absInputPath):
        print(f"{absInputPath} is not a file")
        exit(1)

    df: DataFrame = readDB(dbPath=absInputPath)

    classifications: chain
    match classificationName:
        case "nature-subjects":
            classifications = itertools.chain(NATURE_SUBJECTS.keys())
        case "nature-topics":
            classifications = itertools.chain.from_iterable(
                NATURE_SUBJECTS.values()
            )
        case "scopus-subjects":
            classifications = itertools.chain(SCOPUS_SUBJECTS.keys())
        case "scopus-topics":
            classifications = itertools.chain.from_iterable(
                SCOPUS_SUBJECTS.values()
            )
        case _:
            print("Invalid --classes option")
            exit(1)

    llmRunner: RunnableSequence = buildRunnableSequence(
        classifications=classifications,
        ollamaModel=model,
    )

    data: List[Tuple[int, str]] = inference(
        df=df,
        llmRunner=llmRunner,
        tagName=classificationName,
        model=model,
    )

    writeTagsToFile(data=data, filepaths=df["filename"])


if __name__ == "__main__":
    main()
