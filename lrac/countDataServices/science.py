from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from json import dump
from os import listdir
from pathlib import Path
from typing import Generator, List

import click
from bs4 import BeautifulSoup
from progress.bar import Bar
from pyfs import resolvePath
from toi import chat


def extractText(files: List[Path]) -> List[str]:
    with Bar("Extracting data and code hosting services...", max=len(files)) as bar:

        def _getContent(file: Path) -> str:
            soup: BeautifulSoup = BeautifulSoup(
                markup=open(file, "r"),
                features="lxml",
            )
            content: str = soup.find(
                name="div", attrs={"class": "article-container"}
            ).text
            bar.next()
            return content

        with ThreadPoolExecutor() as executor:
            contentGenerator: Generator = executor.map(_getContent, files)

    data: List[str] = [content for content in contentGenerator]

    return data


def extractDataService(contentList: List[str], token: str) -> defaultdict:
    data: defaultdict = defaultdict(int)

    with Bar(
        "Using GPT4 to analyze how data is shared...", max=len(contentList)
    ) as bar:
        content: str
        for content in contentList:
            response: dict = chat(
                text=content,
                systemPrompt="Identify how data is shared in this research article. Return only the method or service used in JSON format",
                apiKey=token,
                model="gpt-4-0125-preview",
            )

            value: str
            for value in response.values():
                data[value] += 1

            bar.next()

    return data


@click.command()
@click.option(
    "-i",
    "--input",
    "token",
    type=str,
    required=True,
    help="OpenAI token",
)
def main(token: str) -> None:
    directory: Path = resolvePath(path=Path("../../data/science/html/papers"))
    fileList: List[Path] = [
        resolvePath(path=Path(directory, file)) for file in listdir(path=directory)
    ]

    contentList: List[str] = extractText(files=fileList)

    dataServices: defaultdict = extractDataService(
        contentList=contentList,
        token=token,
    )

    with open("scienceDataServices.json", "w") as jsonFile:
        dump(obj=dataServices, fp=jsonFile, indent=4)
        jsonFile.close()


if __name__ == "__main__":
    main()
