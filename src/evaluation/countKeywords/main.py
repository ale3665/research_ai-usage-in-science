from pathlib import Path
from sqlite3 import Connection, connect
from typing import List

import click
import pandas
from pandas import DataFrame, Series
from progress.bar import Bar
from pyfs import isFile, resolvePath

from src.classes import SEARCH_QUERIES


def readDB(dbPath: Path) -> DataFrame:
    sql: str = "SELECT title, summary, document FROM zettels"
    conn: Connection = connect(database=dbPath)
    df: DataFrame = pandas.read_sql_query(sql=sql, con=conn)
    conn.close()
    return df


def countKeyword(data: Series, keyword: str) -> int:
    return data.str.count(pat=keyword).sum()


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
    "-o",
    "--output",
    "outputPath",
    type=Path,
    required=True,
    help="Path to store data in CSV format",
)
def main(inputPath: Path, outputPath: Path) -> None:
    absInputPath: Path = resolvePath(path=inputPath)
    absOutputPath: Path = resolvePath(path=outputPath)

    if not isFile(path=absInputPath):
        print(f"{absInputPath} is not a file")
        exit(1)

    if isFile(path=absOutputPath):
        print(f"{absOutputPath} exists")
        exit(1)

    keywords: List[str] = [kw.strip('"') for kw in SEARCH_QUERIES]
    data: dict[str, List[int]] = {kw: [] for kw in keywords}

    df: DataFrame = readDB(dbPath=absInputPath)
    titleDF: Series[str] = df["title"]
    summaryDF: Series[str] = df["summary"]
    documentDF: Series[str] = df["document"]

    with Bar(
        "Counting the number of keywords per zettel...", max=len(keywords)
    ) as bar:
        kw: str
        for kw in keywords:
            sums: List[int] = []
            sums.append(countKeyword(data=titleDF, keyword=kw))
            sums.append(countKeyword(data=summaryDF, keyword=kw))
            sums.append(countKeyword(data=documentDF, keyword=kw))

            data[kw].append(sum(sums))
            print(data)
            bar.next()

    sumDF: DataFrame = DataFrame(data=data)
    sumDF.to_csv(path_or_buf=absOutputPath, index=False)


if __name__ == "__main__":
    main()
