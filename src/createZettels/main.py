from collections import namedtuple
from pathlib import Path
from subprocess import PIPE, CompletedProcess, Popen  # nosec
from typing import List

import click
import pandas
from bs4 import BeautifulSoup
from pandas import DataFrame
from progress.bar import Bar
from pyfs import isDirectory, isFile, resolvePath

from src.classes.journalGeneric import Journal_ABC
from src.classes.plos import PLOS
from src.utils import storeStringInTempFile

ZETTEL = namedtuple(
    typename="zettel",
    field_names=[
        "doi",
        "title",
        "abstract",
        "document",
        "tag",
        "path",
    ],
)


def extractContent(
    journal: Journal_ABC, df: DataFrame, outputDir: Path
) -> List[ZETTEL]:
    data: List[ZETTEL] = []

    dois: List[str] = []
    titles: List[str] = []
    abstracts: List[str] = []
    documents: List[str] = []
    tags: List[List[str]] = []
    paths: List[Path] = []

    with Bar("Extracting DOIs...", max=df.shape[0]) as bar:
        url: str
        for url in df["url"]:
            doi: str = journal.extractDOIFromPaper(url=url)
            dois.append(doi)

            fp: Path = Path(outputDir, doi.replace("/", "_") + ".yaml")
            paths.append(fp)

            bar.next()

    with Bar("Extracting HTML Content", max=df.shape[0]) as bar:
        html: bytes
        for html in df["html"]:
            soup: BeautifulSoup = BeautifulSoup(markup=html, features="lxml")

            titles.append(journal.extractTitleFromPaper(soup=soup))
            abstracts.append(journal.extractAbstractFromPaper(soup=soup))
            documents.append(journal.extractContentFromPaper(soup=soup))
            tags.extend(journal.extractJournalTagsFromPaper(soup=soup))

            bar.next()

    with Bar("Creating Zettels...", max=df.shape[0]) as bar:
        idx: int
        for idx in range(df.shape[0]):
            zettel: ZETTEL = ZETTEL(
                doi=dois[idx],
                title=titles[idx],
                abstract=abstracts[idx],
                document=documents[idx],
                tag=tags[idx],
                path=paths[idx],
            )

            data.append(zettel)

            bar.next()

    return data


def createZettels(zettels: List[ZETTEL]) -> None:
    """
    Writes a list of ZETTEL objects to disk.

    This function iterates over a list of ZETTEL objects, creates temporary files
    for their titles and abstracts, constructs a shell command to save the ZETTEL
    data to disk, and executes the command. It uses a progress bar to indicate the
    progress of the operation.

    :param zettels: A list of ZETTEL objects to be written to disk.
    :type zettels: List[ZETTEL]
    """  # noqa: E501
    with Bar("Writing Zettels to disk..", max=len(zettels)) as bar:
        zettel: ZETTEL
        for zettel in zettels:
            titleTFName: str = storeStringInTempFile(string=zettel.title)
            abstractTFName: str = storeStringInTempFile(
                string=zettel.abstract,
            )
            contentTFName: str = storeStringInTempFile(string=zettel.document)

            url: str = f"https://doi.org/{zettel.doi.replace('_', '/')}"
            cmd: str = (
                f'zettel --set-url {url} \
                        --load-document {contentTFName} \
                        --load-summary {abstractTFName} \
                        --load-title {titleTFName} \
                        --save "{zettel.path}" \
                        --append-tags {" ".join(zettel.tag).strip()}'
            )

            process: CompletedProcess = Popen(
                cmd,
                shell=True,
                stdout=PIPE,
            )  # nosec

            if process.returncode is not None:
                print(zettel.doi)

            bar.next()


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
    """
    Main function to read a DataFrame, extract content based on the journal,
    and create ZETTEL objects.

    This function performs the following operations:
    1. Resolves the absolute paths for input and output directories.
    2. Checks if the input path is a valid file and the output path is a valid directory.
    3. Reads the input file into a DataFrame.
    4. Determines the journal name from the DataFrame.
    5. Extracts content based on the journal name.
    6. Creates ZETTEL objects and writes them to disk.

    :param inputPath: The path to the input file containing the DataFrame.
    :type inputPath: Path
    :param outputDir: The directory where the output files will be stored.
    :type outputDir: Path
    """  # noqa: E501
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

    data: List[ZETTEL]
    match journalName:
        case "PLOS":
            journal: Journal_ABC = PLOS()
        case _:
            print("Unsupported journal")
            exit(1)

    data: List[ZETTEL] = extractContent(
        journal=journal,
        df=df,
        outputDir=absOutputDirPath,
    )

    createZettels(zettels=data)


if __name__ == "__main__":
    main()
