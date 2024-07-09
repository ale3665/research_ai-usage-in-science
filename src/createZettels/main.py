import re
from collections import namedtuple
from pathlib import Path
from subprocess import PIPE, Popen  # nosec
from tempfile import NamedTemporaryFile
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

ZETTEL = namedtuple(
    typename="zettel",
    field_names=[
        "doi",
        "title",
        "abstract",
        "document",
        "tags",
        "path",
    ],
)


def formatText(string: str) -> str:
    string = re.sub(pattern=r"-\n", repl="", string=string)
    string = string.replace("\n", "")
    string = " ".join(string.split())
    return string


def runZettel(zettel: ZETTEL) -> bool:
    summaryTemp: NamedTemporaryFile = NamedTemporaryFile(
        mode="w+t", delete=False
    )
    noteTemp: NamedTemporaryFile = NamedTemporaryFile(mode="w+t", delete=False)

    summaryTemp.write(zettel.abstract)
    noteTemp.write(zettel.document)

    summaryTemp.close()
    noteTemp.close()

    url: str = f"https://doi.org/{zettel.doi.replace('_', '/')}"
    cmd: str = (
        f'zettel --set-title "{zettel.title}" \
                --set-url {url} \
                --load-summary {summaryTemp.name} \
                --load-note {noteTemp.name} \
                --append-tags {" ".join(zettel.tags).strip()} \
                --save "{zettel.path}"'
    )

    process: Popen[bytes] = Popen(cmd, shell=True, stdout=PIPE)  # nosec

    if process.returncode == 0:
        return True
    else:
        return False


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

            title = formatText(string=title)
            abstract = formatText(string=abstract)

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

    # data: List[ZETTEL] = []

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
