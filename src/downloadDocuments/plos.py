from json import load
from os import listdir
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from progress.bar import Bar
from pyfs import resolvePath
from requests import Response, get

PLOS_SUFFIX: str = "https://journals.plos.org"


def identifyFiles(directory: Path) -> List[Path]:
    data: List[Path] = []

    file: str
    for file in listdir(path=directory):
        foo: Path = Path(directory, file)
        data.append(foo)

    return data


def downloadData(documents: List[dict], storageDirectory: Path) -> None:
    with Bar("Downloading HTML files...", max=len(documents)) as bar:
        document: dict
        for document in documents:
            filename: str = document["id"].replace("/", "_") + ".html"
            filepath: Path = Path(storageDirectory, filename)
            url: str = PLOS_SUFFIX + document["link"]

            response: Response = get(url=url)

            if response.status_code == 200:
                soup: BeautifulSoup = BeautifulSoup(
                    markup=response.content,
                    features="lxml",
                )
                with open(file=filepath, mode="w") as htmlFile:
                    htmlFile.write(soup.prettify())
                    htmlFile.close()

            else:
                print("\n", url, response.status_code)

            bar.next()


def main() -> None:
    jsonDirectory: Path = Path("../../data/json/plos")
    absJSONDirectory: Path = resolvePath(path=jsonDirectory)

    documentDirectory: Path = Path("../../data/documents/plos")
    absDocumentDirectory: Path = resolvePath(path=documentDirectory)

    absDocumentDirectory.mkdir(parents=True, exist_ok=True)

    files: List[Path] = identifyFiles(directory=absJSONDirectory)

    file: Path
    for file in files:
        json: dict = load(fp=open(file))
        docs: List[dict] = json["searchResults"]["docs"]
        downloadData(documents=docs, storageDirectory=absDocumentDirectory)


if __name__ == "__main__":
    main()
