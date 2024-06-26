from pathlib import Path
from typing import List

import click
import pandas
from bs4 import BeautifulSoup, Tag
from pandas import DataFrame, Series
from progress.bar import Bar
from pyfs import isDirectory, isFile, resolvePath

# from src.journals import Journal_ABC
# from src.journals.nature import Nature

# from zettelgeist.zettel import Zettel


def extractPLOSContent(df: DataFrame) -> DataFrame:
    data: dict[str, List] = {"title": [], "summary": [], "url": []}

    with Bar("Extracting content...", max=df.shape[0]) as bar:
        row: Series
        for _, row in df.iterrows():
            soup: BeautifulSoup = BeautifulSoup(
                markup=row["html"],
                features="lxml",
            )

            title: str = soup.find(
                name="h1", attrs={"id": "artTitle"}
            ).text.title()

            abstractContainer: Tag = soup.find(
                name="div", attrs={"class": "abstract-content"}
            )
            abstract: str = abstractContainer.findChild(name="p").text

            data["title"].append(title)
            data["summary"].append(abstract)
            data["url"].append(row["url"])
            bar.next()

    return DataFrame(data=data)


# def createZettels(df: DataFrame) -> None:
#     z: Zettel = Zettel(data)


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a journal's paper parquet file",
)
@click.option(
    "-o",
    "--output",
    "outputDir",
    type=Path,
    required=True,
    help="Directory to save Zettels to",
)
def main(inputPath: Path, outputDir: Path) -> None:
    absInputPath: Path = resolvePath(path=inputPath)
    absOutputDirPath: Path = resolvePath(path=outputDir)

    if not isFile(path=absInputPath):
        print(f"{absInputPath} is not a file")
        exit(1)

    if not isDirectory(path=absOutputDirPath):
        print(f"{absOutputDirPath} is not a directory")
        exit(1)

    print(f"Reading {absInputPath} ...")
    df: DataFrame = pandas.read_parquet(path=absInputPath, engine="pyarrow")
    journalName: str = df["journal"][0]

    match journalName:
        case "Nature":
            print("Hel;lo")
        case "PLOS":
            extractPLOSContent(df=df)
        # case "Science":
        #     journal = Science()
        case _:
            print("Unsupported journal")
            exit(1)


if __name__ == "__main__":
    main()
