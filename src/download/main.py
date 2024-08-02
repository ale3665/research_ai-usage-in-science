from pathlib import Path
from typing import List

import click
import pandas
from pandas import DataFrame
from progress.bar import Bar
from pyfs import isDirectory, isFile, resolvePath
from requests import Response, get

from src.downloadPapers import Journal_ABC
from src.downloadPapers.nature import Nature
from src.downloadPapers.plos import PLOS


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a journal's search result parquet file",
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    type=Path,
    required=True,
    help="Path to save journal paper parquet file",
)
def main(inputPath: Path, outputPath: Path) -> None:
    """
    Reads a DataFrame from a Parquet file, identifies and downloads papers based
    on journal type, and saves the results to a new Parquet file.

    This function performs the following operations:
    1. Resolves the absolute paths for input and output files.
    2. Checks if the input path is a valid file and not a directory, and if the output
       path does not already exist as a file or directory.
    3. Reads the input file into a DataFrame.
    4. Identifies the most common journal name in the DataFrame.
    5. Extracts paper URLs from the HTML content based on the journal type.
    6. Downloads the papers and stores the results.
    7. Saves the results to a new Parquet file.

    :param inputPath: The path to the input file containing the DataFrame.
    :type inputPath: Path
    :param outputPath: The path where the output file will be stored.
    :type outputPath: Path
    """  # noqa: E501
    absInputPath: Path = resolvePath(path=inputPath)
    absOutputPath: Path = resolvePath(path=outputPath)

    if not isFile(path=absInputPath):
        print(f"{absInputPath} is not a file")
        exit(1)

    if isFile(path=absOutputPath):
        print(f"{absOutputPath} is already exists")
        exit(1)

    if isDirectory(path=absInputPath):
        print(f"{absInputPath} is a directory")
        exit()

    if isDirectory(path=absOutputPath):
        print(f"{absOutputPath} is a directory")
        exit()

    data: dict[str, List[str | int | bytes]] = {
        "journal": [],
        "url": [],
        "status_code": [],
        "html": [],
    }

    df: DataFrame = pandas.read_parquet(path=absInputPath, engine="pyarrow")
    journalName: str = df["journal"].value_counts().idxmax()
    resultCount: int = df.shape[0]

    journal: Journal_ABC
    match journalName:
        case "Nature":
            journal = Nature()
        case "PLOS":
            journal = PLOS()
        case _:
            print("Unsupported journal")
            exit(1)

    paperURLs: List[str] = []
    with Bar("Identifying papers from HTML...", max=resultCount) as bar:
        html: str
        for html in df["html"]:
            paperURLs.extend(journal.getPaperURLs(html=html))
            bar.next()

    with Bar("Downloading papers...", max=len(paperURLs)) as bar:
        url: str
        for url in paperURLs:
            data["journal"].append(journal)
            data["url"].append(url)

            resp: Response = get(url=url, timeout=60)

            data["status_code"].append(resp.status_code)
            data["html"].append(resp.content)

            bar.next()

    outputDF: DataFrame = DataFrame(data=data)
    outputDF.to_parquet(path=absOutputPath, engine="pyarrow")


if __name__ == "__main__":
    main()
