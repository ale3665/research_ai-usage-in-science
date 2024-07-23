from pathlib import Path
from sqlite3 import Connection, connect
from typing import List

import click
import pandas
from pandas import DataFrame, Series
from progress.bar import Bar
from pyfs import isFile, resolvePath

from src.utils.search import SEARCH_QUERIES


def readDB(dbPath: Path) -> DataFrame:
    sql: str = "SELECT title, summary, document FROM zettels"
    conn: Connection = connect(database=dbPath)
    df: DataFrame = pandas.read_sql_query(sql=sql, con=conn)
    df["title"] = df["title"].str.lower().replace('\n', ' ')
    df["summary"] = df["summary"].str.lower().replace('\n', ' ')
    df["document"] = df["document"].str.lower().replace('\n', ' ')
    df["combined"] = df["title"] + " " + df["summary"] + " " + df["document"]
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

    keywords: List[str] = [kw.strip('"').lower() for kw in SEARCH_QUERIES]
    data: dict[str, dict[str, List[int]]] = {
    kw: {"title": [], "summary": [], "document": [], "combined": []} for kw in keywords
    }
    

    df: DataFrame = readDB(dbPath=absInputPath)
    titleDF: Series[str] = df["title"]
    summaryDF: Series[str] = df["summary"]
    documentDF: Series[str] = df["document"]
    combinedDF: Series[str] = titleDF + " " + summaryDF + " " + documentDF
    
    with Bar("Counting the number of keywords per zettel...", max=len(keywords)) as bar:
        for kw in keywords:
            title_count = countKeyword(data=titleDF, keyword=kw)
            summary_count = countKeyword(data=summaryDF, keyword=kw)
            document_count = countKeyword(data=documentDF, keyword=kw)
            combined_count = countKeyword(data=combinedDF, keyword=kw)

            data[kw]["title"].append(title_count)
            data[kw]["summary"].append(summary_count)
            data[kw]["document"].append(document_count)
            data[kw]["combined"].append(combined_count)

            bar.next()

    # Transform the data dictionary into a DataFrame for exporting
    csv_data = { 
        "keyword": [],
        "title": [],
        "summary": [],
        "document": [],
        "combined": []
    }

    for kw in keywords:
        csv_data["keyword"].append(kw)
        csv_data["title"].append(sum(data[kw]["title"]))
        csv_data["summary"].append(sum(data[kw]["summary"]))
        csv_data["document"].append(sum(data[kw]["document"]))
        csv_data["combined"].append(sum(data[kw]["combined"]))

    sumDF: DataFrame = DataFrame(csv_data)
    sumDF.to_csv(path_or_buf=absOutputPath, index=False)



if __name__ == "__main__":
    main()
