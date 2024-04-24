from collections import namedtuple
from os import listdir
from pathlib import Path
from subprocess import PIPE, Popen
from typing import List

from bs4 import BeautifulSoup
from progress.bar import Bar
from pyfs import resolvePath

from lrac.createZettels import SEARCH_QUERIES

ZETTEL = namedtuple(
    typename="zettel", field_names=["doi", "title", "abstract", "tags", "path"]
)


def runZettel(zettel: ZETTEL) -> bool:
    cmd: str = f'zettel --set-title "{zettel.title}" --set-url "https://doi.org/{zettel.doi.replace("_", "/")}" \
                --set-note "{zettel.abstract}" \
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
    abstract: str = soup.find(name="section", attrs={"id": "abstract"}).getText(
        separator=" ",
        strip=True,
    )
    return abstract


def extractDocumentTags(soup: BeautifulSoup) -> List[str]:
    tags: List[str] = []
    try:
        tags = [
            "doc:"
            + soup.find(name="div", attrs={"class": "meta-panel__overline"})
            .getText(strip=True)
            .lower()
            .replace(" ", "_")
        ]
    except AttributeError:
        tags = [
            "doc:"
            + soup.find(name="div", attrs={"class": "meta-panel__type"})
            .getText(strip=True)
            .lower()
            .replace(" ", "_")
        ]
    return tags


def extractSearchQueryTags(
    soup: BeautifulSoup,
    searchQueries: List[str] = SEARCH_QUERIES,
) -> List[str]:
    tags: List[str] = []
    documentText: str = " ".join(
        soup.find(name="article")
        .get_text(separator=" ", strip=True)
        .replace("\n", " ")
        .lower()
        .split(sep=" ")
    )

    query: str
    for query in searchQueries:
        query = query.lower()
        if query in documentText:
            tags.append("search:" + query.replace(" ", "_"))

    return tags


def main() -> None:
    data: List[ZETTEL] = []
    zettelDir: Path = resolvePath(path=Path("../../data/science/zettlegeist/zettels"))
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
            docTags: List[str] = extractDocumentTags(soup=soup)
            searchTags: List[str] = extractSearchQueryTags(soup=soup)

            tags: List[str] = docTags + searchTags

            docZettel: ZETTEL = ZETTEL(
                doi=doi,
                title=title,
                abstract=abstract,
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
