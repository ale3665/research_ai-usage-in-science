from pathlib import Path
from sqlite3 import Connection, connect
from typing import Hashable, List, Tuple

import click
import pandas
from pandas import DataFrame, Series
from progress.bar import Bar
from pyfs import isFile, resolvePath
from requests import Response

from src.classes.openalex import OpenAlex


def readDB(dbPath: Path) -> DataFrame:
    sqlQuery: str = "SELECT * FROM zettels"
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
            tagStor: List[str] = []

            doi: str = row["url"]

            resp: Response = oa.searchByDOI(doiURL=doi)
            tags: DataFrame = oa.getWorkTopics(resp=resp)

            for tagIDX, tagRow in tags.iterrows():
                tags: List[str] = []

                tags.append(
                    f"\"OpenAlex_topic_{tagIDX}_{tagRow['topic']}\"",
                )
                tags.append(
                    f"\"OpenAlex_subfield_{tagIDX}_{tagRow['subfield']}\"",
                )
                tags.append(
                    f"\"OpenAlex_field_{tagIDX}_{tagRow['field']}\"",
                )

                tagStor.append(" ".join(tags))

            data.append((idx, " ".join(tagStor)))
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

    df: DataFrame = readDB(dbPath=absInputPath)

    data: List[Tuple[int, str]] = getTags(df=df)

    print(data)


if __name__ == "__main__":
    main()
