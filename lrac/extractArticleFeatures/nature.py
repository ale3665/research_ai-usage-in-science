from os import listdir
from os.path import dirname
from pathlib import Path
from typing import List

import click
import pandas
from bs4 import BeautifulSoup
from pandas import DataFrame
from progress.bar import Bar
from pyfs import isDirectory, listDirectory, resolvePath

DEFAULT_INPUT_DIRECTORY: Path = resolvePath(path=Path("../../data/nature/html/papers"))
DEFAULT_OUTPUT: Path = resolvePath(path=Path("../../data/nature/csv/paperFeatures.csv"))


def extractFeatures(doi: str, soup: BeautifulSoup) -> DataFrame:
    data: dict[str, List[str]] = {
        "doi": [doi],
        "title": [],
        "abstract": [],
    }

    title: str = soup.find(name="h1", attrs={"class": "c-article-title"}).get_text(
        strip=True
    )

    abstract: str
    try:
        abstract = soup.find(name="div", attrs={"id": "Abs1-content"}).get_text(
            strip=True
        )
    except AttributeError:
        abstract = ""

    data["title"].append(title)
    data["abstract"].append(abstract)

    return DataFrame(data=data)


def checkDirectoryExistence(directory: Path, mkdir: bool = False) -> None:
    if isDirectory(path=directory) == False:
        if mkdir:
            directory.mkdir(parents=True, exist_ok=True)
        else:
            print("Invalid directory input")
            print(directory)
            quit(1)


@click.command()
@click.option(
    "-i",
    "--input-directory",
    "input_",
    default=DEFAULT_INPUT_DIRECTORY,
    show_default=True,
    help="Path to the directory containing downloaded Nature articles in HTML format",
    type=Path,
)
@click.option(
    "-o",
    "--output-directory",
    "output",
    default=DEFAULT_OUTPUT,
    show_default=True,
    help="Path to the directory to store paper features",
    type=Path,
)
def main(input_: Path, output: Path) -> None:
    userInput: Path = resolvePath(path=input_)
    userOutput: Path = resolvePath(path=output)

    checkDirectoryExistence(directory=userInput)
    checkDirectoryExistence(directory=Path(dirname(p=userOutput)), mkdir=True)

    fileList: List[Path] = listDirectory(path=userInput)

    dfs: List[DataFrame] = []
    with Bar("Extracting features...", max=len(fileList)) as bar:
        filepath: Path
        for filepath in fileList:
            doi: str = filepath.stem.replace("_", "/")
            with open(file=filepath, mode="r") as htmlFile:
                soup: BeautifulSoup = BeautifulSoup(
                    markup=htmlFile,
                    features="lxml",
                )
                dfs.append(extractFeatures(doi=doi, soup=soup))
                htmlFile.close()
            bar.next()

    df: DataFrame = pandas.concat(objs=dfs, ignore_index=True)
    df.to_csv(path_or_buf=userOutput, index=False)


if __name__ == "__main__":
    main()
