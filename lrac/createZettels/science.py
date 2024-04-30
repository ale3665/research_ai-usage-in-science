import re
from collections import namedtuple
from os import listdir
from pathlib import Path
from subprocess import PIPE, Popen
from tempfile import NamedTemporaryFile
from typing import List

from bs4 import BeautifulSoup, Tag
from progress.bar import Bar
from pyfs import resolvePath

from lrac.createZettels import SEARCH_QUERIES

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
    summaryTemp: NamedTemporaryFile = NamedTemporaryFile(mode="w+t", delete=False)
    noteTemp: NamedTemporaryFile = NamedTemporaryFile(mode="w+t", delete=False)

    summaryTemp.write(zettel.abstract)
    noteTemp.write(zettel.document)

    summaryTemp.close()
    noteTemp.close()

    url: str = f"https://doi.org/{zettel.doi.replace('_', '/')}"
    cmd: str = f'zettel --set-title "{zettel.title}" \
                --set-url {url} \
                --load-summary {summaryTemp.name} \
                --load-note {noteTemp.name} \
                --append-tags {" ".join(zettel.tags).strip()} \
                --save "{zettel.path}"'

    process: Popen[bytes] = Popen(cmd, shell=True, stdout=PIPE)

    if process.returncode == 0:
        return True
    else:
        return False


def extractTitle(soup: BeautifulSoup) -> str:
    title: str = soup.find(name="h1", attrs={"property": "name"}).text.strip()
    return title


def extractAbstract(soup: BeautifulSoup) -> str:
    abstractContainer: Tag = soup.find(
        name="section",
        attrs={"id": "abstract"},
    )
    abstractParagraph: Tag = abstractContainer.find(
        name="div",
        attrs={"role": "paragraph"},
    )
    abstractText: str = abstractParagraph.text
    return formatText(string=abstractText)


def extractDocumentTags(soup: BeautifulSoup) -> List[str]:
    tagSuffix: str = "doc-"
    tags: List[str] = []
    try:
        tags = [
            tagSuffix
            + soup.find(name="div", attrs={"class": "meta-panel__overline"}).getText(
                strip=True
            )
        ]
    except AttributeError:
        tags = [
            tagSuffix
            + soup.find(name="div", attrs={"class": "meta-panel__type"}).getText(
                strip=True
            )
        ]

    formattedTags: List[str] = [f'"{tag.lower().strip()}"' for tag in tags]
    return formattedTags


def extractDocument(soup: BeautifulSoup) -> str:
    documentTag: Tag = soup.find(name="section", attrs={"id": "bodymatter"})
    documentText: str = documentTag.text
    documentText = formatText(string=documentText)
    return documentText


def extractSearchQueryTags(
    documentText: str,
    searchQueries: List[str] = SEARCH_QUERIES,
) -> List[str]:
    tags: List[str] = []
    documentText = documentText.lower()

    query: str
    for query in searchQueries:
        query = query.lower()
        if query in documentText:
            tags.append("search-" + query)

    formattedTags: List[str] = [f'"{tag.lower().strip()}"' for tag in tags]
    return formattedTags


def main() -> None:
    data: List[ZETTEL] = []
    zettelDir: Path = resolvePath(
        path=Path("../../data/science/zettelgeist/zettels"),
    )
    htmlDir: Path = resolvePath(path=Path("../../data/science/html/papers"))
    htmlFiles: List[Path] = [
        resolvePath(path=Path(htmlDir, file)) for file in listdir(path=htmlDir)
    ]

    with Bar("Creating zettels from HTML files...", max=len(htmlFiles)) as bar:
        filepath: Path
        for filepath in htmlFiles:
            doi: str = filepath.stem.strip()
            zettelFile: Path = Path(zettelDir, doi + ".yaml")
            with open(file=filepath, mode="r") as htmlFile:
                soup: BeautifulSoup = BeautifulSoup(
                    markup=htmlFile,
                    features="lxml",
                )
                htmlFile.close()

            title: str = extractTitle(soup=soup)
            abstract: str = extractAbstract(soup=soup)
            documentText: str = extractDocument(soup=soup)
            docTags: List[str] = extractDocumentTags(soup=soup)
            searchTags: List[str] = extractSearchQueryTags(
                documentText=f"{title} {abstract} {documentText}",
            )

            tags: List[str] = docTags + searchTags

            docZettel: ZETTEL = ZETTEL(
                doi=doi,
                title=title,
                abstract=abstract,
                document=documentText,
                tags=tags,
                path=zettelFile.__str__(),
            )
            data.append(docZettel)

            returnCode: int = runZettel(zettel=docZettel)
            if returnCode == 0:
                pass
            else:
                print("Error:", doi)

            bar.next()


if __name__ == "__main__":
    main()
