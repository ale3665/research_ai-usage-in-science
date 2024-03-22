from os import listdir
from pathlib import Path
from typing import List, Set

from bs4 import BeautifulSoup, ResultSet, Tag
from pandas import DataFrame
from progress.bar import Bar
from pyfs import resolvePath


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


def createDataStructure(bucketKeys: List[str]) -> dict[str, List[int]]:
    data: dict[str, List[int]] = {}
    uniqueKeys: Set[str] = set([])

    key: str
    for key in bucketKeys:
        splitKey: List[str] = key.split(sep=" ")
        uniqueKeys.add(" ".join(splitKey[0:-1]))

    for key in uniqueKeys:
        data[key] = []

    return dict(sorted(data.items()))


def evaluateData(filepaths: List[Path]) -> int:
    documentCount: int = 0

    file: Path
    for file in filepaths:
        soup: BeautifulSoup = BeautifulSoup(markup=open(file), features="lxml")
        documentCount += len(soup.find_all(name="h3", attrs={"class": "c-card__title"}))

    return documentCount


def main() -> None:
    dataDirectory: Path = resolvePath(path=Path("../../../data/html/nature"))
    filesUnformatted: List[str] = listdir(path=dataDirectory)
    filesFormatted: List[Path] = [
        resolvePath(path=Path(dataDirectory, file)) for file in filesUnformatted
    ]
    htmlFiles: List[Path] = [file for file in filesFormatted if file.suffix == ".html"]

    buckets: dict[str, List[Path]] = createBuckets(filepaths=htmlFiles)
    bucketKeys: List[str] = list(buckets.keys())

    data: dict[str, List[int]] = createDataStructure(bucketKeys=bucketKeys)

    bucket: str
    with Bar("Counting publications per bucket...", max=len(bucketKeys)) as bar:
        for bucket in bucketKeys:
            dataKey: str = " ".join(bucket.split(sep=" ")[0:-1])
            count: int = evaluateData(filepaths=buckets[bucket])
            data[dataKey].append(count)
            bar.next()

    DataFrame(data=data, index=[2015 + i for i in range(0, 10)]).T.to_csv(
        path_or_buf="naturePaperCount.csv",
        index=True,
    )


if __name__ == "__main__":
    main()
