import re
from collections import namedtuple
from pathlib import Path
from subprocess import PIPE, CompletedProcess, Popen  # nosec
from tempfile import NamedTemporaryFile
from typing import List

import click
import pandas
from bs4 import BeautifulSoup, Tag
from pandas import DataFrame
from progress.bar import Bar
from pyfs import isDirectory, isFile, resolvePath

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


def _formatText(string: str) -> str:
    """
    Formats a given string by removing certain characters and cleaning up whitespace.

    This function performs the following operations on the input string:
    1. Removes hyphenated newlines (i.e., "-\n").
    2. Replaces newlines with an empty string.
    3. Collapses multiple spaces into a single space.

    :param string: The input string to be formatted.
    :type string: str
    :return: The formatted string with cleaned-up text.
    :rtype: str
    """  # noqa: E501
    string = re.sub(pattern=r"-\n", repl="", string=string)
    string = string.replace("\n", "")
    string = " ".join(string.split())
    return string


def _storeStringInTempFile(string: str) -> str:
    """
    Stores a given string in a temporary file and returns the file's name.

    This function creates a temporary file, writes the given string to it,
    and returns the name of the temporary file. The temporary file is not
    deleted when closed, allowing the caller to access it later.

    :param string: The input string to be stored in the temporary file.
    :type string: str
    :return: The name of the temporary file containing the stored string.
    :rtype: str
    """
    tf: NamedTemporaryFile = NamedTemporaryFile(
        mode="w+t",
        delete=False,
    )

    tfName: str = tf.name

    tf.write(string)
    tf.close()

    return tfName


def _extractDOI_PLOS(url: str) -> str:
    """
    Extracts the DOI from a PLOS article URL.

    This function takes a PLOS article URL and extracts the DOI by splitting
    the URL at the '=' character and returning the second part.

    :param url: The URL of the PLOS article.
    :type url: str
    :return: The extracted DOI from the URL.
    :rtype: str
    """
    splitURL: List[str] = url.split(sep="=")
    return splitURL[1]


def _extractTitle_PLOS(soup: BeautifulSoup) -> str:
    """
    Extracts the title of a PLOS article from a BeautifulSoup object.

    This function takes a BeautifulSoup object representing a PLOS article's HTML
    content, finds the title element by its tag and attributes, and returns the
    formatted title text.

    :param soup: A BeautifulSoup object containing the parsed HTML of the PLOS article.
    :type soup: BeautifulSoup
    :return: The formatted title of the PLOS article.
    :rtype: str
    """  # noqa: E501
    title: Tag = soup.find(name="h1", attrs={"id": "artTitle"})
    return _formatText(string=title.text)


def _extractAbstract_PLOS(soup: BeautifulSoup) -> str:
    """
    Extracts the abstract of a PLOS article from a BeautifulSoup object.

    This function takes a BeautifulSoup object representing a PLOS article's HTML
    content, finds the abstract element by its tag and attributes, and returns the
    formatted abstract text.

    :param soup: A BeautifulSoup object containing the parsed HTML of the PLOS article.
    :type soup: BeautifulSoup
    :return: The formatted abstract of the PLOS article.
    :rtype: str
    """  # noqa: E501
    abstract: Tag = soup.find(name="div", attrs={"class": "abstract-content"})
    return _formatText(string=abstract.text)


def extractContnet_PLOS(df: DataFrame, outputDir: Path) -> List[ZETTEL]:
    """
    Extracts content from a PLOS DataFrame and creates a list of ZETTEL objects.

    This function performs the following operations:
    1. Extracts DOIs from URLs in the DataFrame.
    2. Parses HTML content from the DataFrame to extract titles and abstracts.
    3. Creates ZETTEL objects using the extracted information and stores them in a list.

    :param df: The DataFrame containing PLOS article data.
    :type df: DataFrame
    :param outputDir: The directory where the output files will be stored.
    :type outputDir: Path
    :return: A list of ZETTEL objects containing the extracted content.
    :rtype: List[ZETTEL]
    """  # noqa: E501
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
            doi: str = _extractDOI_PLOS(url=url)
            dois.append(doi)

            fp: Path = Path(outputDir, doi.replace("/", "_") + ".yaml")
            paths.append(fp)

            bar.next()

    with Bar("Extracting HTML Content", max=df.shape[0]) as bar:
        html: bytes
        for html in df["html"]:
            soup: BeautifulSoup = BeautifulSoup(markup=html, features="lxml")

            titles.append(_extractTitle_PLOS(soup=soup))
            abstracts.append(_extractAbstract_PLOS(soup=soup))
            documents.append("")
            tags.append([""])

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
            titleTFName: str = _storeStringInTempFile(string=zettel.title)
            abstractTFName: str = _storeStringInTempFile(
                string=zettel.abstract,
            )

            # --load-note {noteTemp.name} \
            # --append-tags {" ".join(zettel.tag).strip()} \
            url: str = f"https://doi.org/{zettel.doi.replace('_', '/')}"
            cmd: str = (
                f'zettel --load-title {titleTFName} \
                        --set-url {url} \
                        --load-summary {abstractTFName} \
                        --save "{zettel.path}"'
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
            data = extractContnet_PLOS(
                df=df,
                outputDir=absOutputDirPath,
            )
        case _:
            print("Unsupported journal")
            exit(1)

    createZettels(zettels=data)


if __name__ == "__main__":
    main()
