from pathlib import Path
from sqlite3 import Connection, connect
from string import Template
from subprocess import PIPE, CompletedProcess, Popen  # nosec
from typing import Hashable, List, Tuple

import click
import pandas
from pandas import DataFrame, Series
from progress.bar import Bar
from pyfs import isFile, resolvePath
from requests import Response

from src.classes.openalex import OpenAlex


def readDB(dbPath: Path) -> DataFrame:
    sqlQuery: str = "SELECT url, filename FROM zettels"
    conn: Connection = connect(database=dbPath)
    df: DataFrame = pandas.read_sql_query(sql=sqlQuery, con=conn)
    conn.close()
    return df


def getTags(
    df: DataFrame,
) -> List[Tuple[int, str]]:
    data: List[Tuple[int, str]] = []
    oa: OpenAlex = OpenAlex()

    with Bar("Getting tags...", max=df.shape[0]) as bar:
        row: Series
        idx: Hashable
        for idx, row in df.iterrows():
            doi: str = row["url"]

            resp: Response = oa.searchByDOI(doiURL=doi)
            tags: DataFrame = oa.getWorkTopics(resp=resp)

            for tagIDX, tagRow in tags.iterrows():
                data.append(
                    (
                        idx,
                        f"OpenAlex_topic_{tagIDX}_{tagRow['topic']}",
                    ),
                )
                data.append(
                    (
                        idx,
                        f"OpenAlex_subfield_{tagIDX}_{tagRow['subfield']}",
                    ),
                )
                data.append(
                    (
                        idx,
                        f"OpenAlex_field_{tagIDX}_{tagRow['field']}",
                    ),
                )

            bar.next()

    return data


def writeTagsToFile(data: List[Tuple[int, str]], filepaths: Series) -> None:
    """
    Writes tags to files based on the provided data and filepaths.

    This function iterates over a list of data tuples containing file indices and
    tags, constructs a command to append the tag to the corresponding file using
    a shell command, and executes the command. It uses a progress bar to indicate
    the progress of the operation.

    :param data: A list of tuples where each tuple contains an index and a tag.
    :type data: List[Tuple[int, str]]
    :param filepaths: A Series containing filepaths indexed by the same indices as in data.
    :type filepaths: Series
    :return: None
    """  # noqa: E501
    cmdTemplate: Template = Template(
        template='zettel --file ${filepath} --append-tag "${tag}" --in-place',
    )

    with Bar("Writing tags to files...", max=len(data)) as bar:
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
def main(inputPath: Path) -> None:
    absInputPath: Path = resolvePath(path=inputPath)

    if not isFile(path=absInputPath):
        print(f"{absInputPath} is not a file")
        exit(1)

    df: DataFrame = readDB(dbPath=absInputPath)

    data: List[Tuple[int, str]] = getTags(df=df)

    writeTagsToFile(data=data, filepaths=df["filename"])


if __name__ == "__main__":
    main()
