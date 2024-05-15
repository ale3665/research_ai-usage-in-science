from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from json import dump
from os import listdir
from pathlib import Path
from typing import Generator, List

from bs4 import BeautifulSoup, ResultSet
from progress.bar import Bar
from pyfs import resolvePath


def extractSubjects(fileList: List[Path]) -> defaultdict:
    data: defaultdict = defaultdict(int)

    with Bar("Extracting subjects per paper...", max=len(fileList)) as bar:

        def _getSubject(file: Path) -> List[str]:
            soup: BeautifulSoup = BeautifulSoup(
                markup=open(file, "r"),
                features="lxml",
            )
            results: ResultSet = soup.find_all(
                name="div",
                attrs={
                    "class": "meta-panel__overline",
                },
            )
            bar.next()
            return [result.text.replace("  ", "").strip().title() for result in results]

        with ThreadPoolExecutor() as executor:
            results: Generator = executor.map(_getSubject, fileList)

    result: List[str]
    subject: str
    for result in results:
        for subject in result:
            data[subject] += 1

    return data


def main() -> None:
    directory: Path = resolvePath(path=Path("../../data/science/html/papers"))
    fileList: List[Path] = [
        resolvePath(path=Path(directory, file)) for file in listdir(path=directory)
    ]
    data: defaultdict = extractSubjects(fileList=fileList)

    with open(
        resolvePath(
            path=Path("../../data/science/json/articlesPerScienctificDomain.json")
        ),
        "w",
    ) as jsonFile:
        dump(obj=data, fp=jsonFile, indent=4)
        jsonFile.close()


if __name__ == "__main__":
    main()
