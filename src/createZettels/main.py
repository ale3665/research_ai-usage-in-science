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
        "tag",
        "path",
    ],
)


def _formatText(string: str) -> str:
    string = re.sub(pattern=r"-\n", repl="", string=string)
    string = string.replace("\n", "")
    string = " ".join(string.split())
    return string


def _storeStringInTempFile(string: str) -> str:
    tf: NamedTemporaryFile = NamedTemporaryFile(
        mode="w+t",
        delete=False,
    )

    tfName: str = tf.name

    tf.write(string)
    tf.close()

    return tfName


def _createSoup(html: bytes) -> BeautifulSoup:
    return BeautifulSoup(markup=html, features="lxml")


def _extractDOI_PLOS(url: str) -> str:
    splitURL: List[str] = url.split(sep="=")
    return splitURL[1]


def _extractTitle_PLOS(soup: BeautifulSoup) -> str:
    title: Tag = soup.find(name="h1", attrs={"id": "artTitle"})
    return _formatText(string=title.text)


def _extractAbstract_PLOS(soup: BeautifulSoup) -> str:
    abstract: Tag = soup.find(name="div", attrs={"class": "abstract-content"})
    return _formatText(string=abstract.text)


def _extractDocument_PLOS(soup: BeautifulSoup) -> str:
    pass


def _extractTags_PLOS(soup: BeautifulSoup) -> str:
    pass


def extractContnet_PLOS(df: DataFrame, outputDir: Path) -> List[ZETTEL]:
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
