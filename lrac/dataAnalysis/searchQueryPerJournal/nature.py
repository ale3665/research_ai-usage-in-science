from os import listdir
from pathlib import Path
from typing import List, Set

from bs4 import BeautifulSoup
from pandas import DataFrame
from progress.bar import Bar

from lrac.utils.fs import resolvePath


def createBuckets(filepaths: List[Path]) -> dict[str, List[Path]]:
    keys: List[str] = []
    uniqueKeys: Set[str] = set([])
    data: dict[str, List[Path]] = {}

    file: Path
    for file in filepaths:
        key: str = file.stem.replace("Nature Search Results", "").replace("  ", " ")
        keys.append(key)

    key: str
    for key in keys:
        splitKey: List[str] = key.split(sep=" ")

        shortKey: str = ""
        if int(splitKey[-1]) < 2015:
            shortKey = " ".join(splitKey[0:-1])
        else:
            shortKey = key

        uniqueKeys.add(shortKey)

    for key in uniqueKeys:
        relevantFiles: List[Path] = [
            file
            for file in filepaths
            if file.stem.replace("Nature Search Results", "")
            .replace("  ", " ")
            .find(key)
            != -1
        ]
        data[key] = relevantFiles

    return dict(sorted(data.items()))


def createDataStructure(bucketKeys: List[str]) -> dict[str, DataFrame]:
    data: dict[str, DataFrame] = {}
    uniqueKeys: Set[str] = set([])

    key: str
    for key in bucketKeys:
        splitKey: List[str] = key.split(sep=" ")
        uniqueKeys.add(" ".join(splitKey[0:-1]))

    for key in uniqueKeys:
        data[key] = DataFrame()

    return dict(sorted(data.items()))


def evaluateData(filepaths: List[Path]) -> int:
    file: Path
    for file in filepaths:
        soup: BeautifulSoup = BeautifulSoup(markup=open(file), features="lxml")
        print(soup.prettify())
        quit()


def main() -> None:
    dataDirectory: Path = resolvePath(path=Path("../../../data/html/nature"))
    filesUnformatted: List[str] = listdir(path=dataDirectory)
    filesFormatted: List[Path] = [
        resolvePath(path=Path(dataDirectory, file)) for file in filesUnformatted
    ]
    htmlFiles: List[Path] = [file for file in filesFormatted if file.suffix == ".html"]

    buckets: dict[str, List[Path]] = createBuckets(filepaths=htmlFiles)
    bucketKeys: List[str] = list(buckets.keys())

    data: dict[str, DataFrame] = createDataStructure(bucketKeys=bucketKeys)

    bucket: str
    for bucket in bucketKeys:
        evaluateData(filepaths=buckets[bucket])


if __name__ == "__main__":
    main()
