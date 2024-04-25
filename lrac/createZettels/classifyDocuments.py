from pathlib import Path
from typing import List, Tuple

import click
import pandas
import sqlalchemy
from langchain_community.llms.ollama import Ollama
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence
from pandas import DataFrame
from progress.bar import Bar
from pyfs import resolvePath
from sqlalchemy import Connection, Engine

from lrac.createZettels import NATURE_BUCKETS

SYSTEM_PROMPT: str = f'Classify the text as one of the following: {", ".join(NATURE_BUCKETS)}. Return as JSON.'


def readDB(dbPath: Path) -> DataFrame:
    dbEngine: Engine = sqlalchemy.create_engine(url=f"sqlite:///{dbPath.__str__()}")
    con: Connection = dbEngine.connect()
    zettels: DataFrame = pandas.read_sql_table(
        table_name="zettels_content",
        con=con,
        index_col="docid",
    )
    con.close()
    return zettels


def inference(llm: Ollama, pairing: Tuple[str, Path]) -> Tuple[Path, str]:
    prompt: str = pairing[0]
    outputParser: JsonOutputParser = JsonOutputParser()
    chatPrompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("user", "{input}"),
        ]
    )

    chain: RunnableSequence = chatPrompt | llm | outputParser

    classification: str
    try:
        response: dict = chain.invoke({"input": prompt})
        classification = (
            llm.model.lower()
            + ":"
            + list(response.values())[0].replace(" ", "_").lower()
        )
    except OutputParserException:
        classification = "llm_erorr"
    except AttributeError:
        classification = "llm_erorr"

    return (pairing[1], classification)


@click.command()
@click.option(
    "-i",
    "--input",
    "inputDB",
    type=Path,
    required=True,
    help="Path to ZettelGiest DB",
)
@click.option(
    "-m",
    "--model",
    "model",
    type=str,
    required=False,
    default="gemma",
    help="Model to perform inference with. NOTE: Must be accessible via Ollama",
)
def main(inputDB: Path, model: str) -> None:
    dbPath: Path = resolvePath(path=inputDB)
    dbPathDir: Path = dbPath.parent

    df: DataFrame = readDB(dbPath=dbPath)
    relevantDF: DataFrame = df[["c0title", "c8note", "c13filename"]]

    data: List[str] = [
        " ".join(i) for i in zip(relevantDF["c0title"], relevantDF["c8note"])
    ]
    dataPathPairings: List[Tuple[str, Path]] = [
        (i[0], Path(dbPathDir, i[1])) for i in zip(data, relevantDF["c13filename"])
    ]

    llm: Ollama = Ollama(model=model)

    with Bar("Classifying data based on title and abstract...", max=len(data)) as bar:
        pair: Tuple[str, Path]
        for pair in dataPathPairings:
            print(inference(llm=llm, pairing=pair))
            bar.next()


if __name__ == "__main__":
    main()
