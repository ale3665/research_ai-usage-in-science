from os import mkdir
from os.path import isdir, isfile
from pathlib import Path
from typing import List, Literal

from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, get


def _replaceText(x: str) -> str:
    y: str = (
        x.strip()
        .replace(" ", "")
        .replace("&", "And")
        .replace("-", "")
        .replace(":", "")
        .replace("'", "")
        .replace(r"\xe2\x80\x94", "")
    )
    return y


class Journal2Class:
    def __init__(
        self,
        baseName: str,
        journalIndexURL: str,
        baseURL: str = "",
        feedType: Literal["api", "atom", "rss"] = "rss",
    ) -> None:
        self.journalBaseName: str = baseName
        self.journalBaseURL: str = baseURL

        self.journalFeedType: Literal["api", "atom", "rss"] = feedType

        self.journalIndexURL: str = journalIndexURL
        self.journalIndexSoup: BeautifulSoup = BeautifulSoup()
        self.journalIndexHTMLPath: Path = Path("html", self.journalBaseName + ".html")

        self.subjournals: dict[str, str] = {}

    def getHTML(self) -> None:
        if isfile(path=self.journalIndexHTMLPath):
            with open(self.journalIndexHTMLPath, "r") as htmlFile:
                self.journalIndexSoup = BeautifulSoup(
                    markup=htmlFile,
                    features="lxml",
                )
                htmlFile.close()

        if isdir(s=self.journalIndexHTMLPath.parent):
            pass
        else:
            mkdir(path=self.journalIndexHTMLPath.parent)

        resp: Response = get(url=self.journalIndexURL)

        with open(self.journalIndexHTMLPath, "w") as htmlFile:
            htmlFile.write(resp.content.__str__())
            htmlFile.close()

        self.journalIndexSoup = BeautifulSoup(
            markup=resp.content,
            features="lxml",
        )

    def identifySubjournals(self, searchQuery: dict[str, str]) -> None:
        """
        Expects search query to be inputted as {'class' : 'attribute'}
        """
        links: ResultSet = self.journalIndexSoup.find_all(
            name="a",
            attrs=searchQuery,
        )

        link: Tag
        for link in links:
            self.subjournals[
                f"{self.journalBaseName} {link.text}"
            ] = self.journalBaseURL + link.get(key="href")

    def buildClass(self) -> str:
        classNames: List[str] = list(self.subjournals.keys())
        urls: List[str] = list(self.subjournals.values())

        formattedClassNames: List[str] = list(map(_replaceText, classNames))

        feedURL: str = f"{url[:-1]}.rss"

        return f"""
    class {className}(Journal):
    def __init__(self)  ->  None:
        self.name= "{name}"
        self.url= "{url}"
        self.feedType= "{feedType}"
        self.feedURL= "{feedURL}"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs)    ->  str:
        if "entryDOI" in kwargs:
            partialDOI: str = kwargs.get("entryDOI").split("/")[1]
            return self.entryDownloadURLTemplate.substitute(partialDOI)
        return ""
"""


def main() -> None:
    soup: BeautifulSoup = getRawNaturePortfolio()
    nameHREFPairs: dict[str, str] = extractRelevantData(soup=soup)

    data: str = ""

    key: str
    for key in nameHREFPairs.keys():
        data += buildClass(name=key, link=nameHREFPairs[key])

    print(data)


if __name__ == "__main__":
    main()
