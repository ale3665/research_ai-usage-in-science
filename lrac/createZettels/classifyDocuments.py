from pathlib import Path
from subprocess import PIPE, Popen
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
            llm.model.lower().replace(":", "_")
            + ":"
            + list(response.values())[0].replace(" ", "_").lower()
        )
    except OutputParserException:
        classification = llm.model.replace(":", "_") + ":" + "llm_erorr_ope"
    except AttributeError:
        classification = llm.model.replace(":", "_") + ":" + "llm_erorr_ae"

    return (pairing[1], classification)


def appendTag(path: Path, tag: str) -> bool:
    cmd: str = f"zettel --file {path.__str__()} \
            --append-tags {tag} \
            --in-place"
    process: Popen[bytes] = Popen(cmd, shell=True, stdout=PIPE)

    if process.returncode == 0:
        return True
    else:
        return False


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
    fileClassifications: List[Tuple[Path, str]] = []

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
            result: Tuple[Path, str] = inference(llm=llm, pairing=pair)
            fileClassifications.append(result)
            bar.next()

    with Bar("Writing data to files...", max=len(fileClassifications)) as bar:
        datum: Tuple[Path, str]
        for datum in fileClassifications:
            updatedFile: bool = appendTag(path=datum[0], tag=datum[1])

            # if updatedFile:
            #     pass
            # else:
            #     print("error:", datum[0].__str__())
            bar.next()


if __name__ == "__main__":
    main()
