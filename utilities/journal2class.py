from abc import ABCMeta, abstractmethod
from os import mkdir
from os.path import isdir, isfile
from pathlib import Path
from typing import List, Literal, Protocol, runtime_checkable

from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, get


@runtime_checkable
class J2C_Protocol(Protocol):
    publisherName: str
    journalIndexURL: str
    htmlSearchQuery: dict[str, str]
    journalFeedBaseURL: str
    journalFeedType: Literal["atom", "rss"]

    journalIndexHTMLPath: Path
    journalIndexSoup: BeautifulSoup
    journalURLMapping: dict[str, str]


class J2C_ABC(J2C_Protocol, metaclass=ABCMeta):
    def __init__(self) -> None:
        self.journalIndexHTMLPath = Path("html", self.publisherName + ".html")

    @classmethod
    def getHTML(cls) -> None:
        if isfile(path=cls.journalIndexHTMLPath):
            with open(cls.journalIndexHTMLPath, "r") as htmlFile:
                cls.journalIndexSoup = BeautifulSoup(
                    markup=htmlFile,
                    features="lxml",
                )
                htmlFile.close()

        if isdir(s=cls.journalIndexHTMLPath.parent):
            pass
        else:
            mkdir(path=cls.journalIndexHTMLPath.parent)

        resp: Response = get(url=cls.journalIndexURL)

        with open(cls.journalIndexHTMLPath, "w") as htmlFile:
            htmlFile.write(resp.content.__str__())
            htmlFile.close()

        cls.journalIndexSoup = BeautifulSoup(
            markup=resp.content,
            features="lxml",
        )

    @abstractmethod
    def parseHTML(self) -> None:
        ...

    @abstractmethod
    def createClasses(self) -> str:
        ...


class Science(J2C_ABC):
    def __init__(self) -> None:
        self.publisherName = "Science"
        self.journalIndexURL = (
            "https://www.science.org/content/page/email-alerts-and-rss-feeds"
        )
        self.htmlSearchQuery = {"class": "advanced-page news-article-content"}
        self.journalFeedBaseURL: str = "https://www.science.org"
        self.journalFeedType = "rss"

        self.journalIndexSoup = BeautifulSoup()
        self.journalURLMapping = {}

        super().__init__()

    def parseHTML(self) -> None:
        links: ResultSet = self.journalIndexSoup.find_all(
            name="a",
            attrs=self.htmlSearchQuery,
        )

        link: Tag
        for link in links:
            self.journalURLMapping[f"{link.text}"] = (
                self.journalFeedBaseURL + link.get(key="href").__str__()
            )

    def createClasses(self) -> str:
        return ""


s = Science()
s.getHTML()
s.parseHTML()
print(s.journalURLMapping)


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


# class _Journal2Class:
#     def __init__(
#         self,
#         baseName: str,
#         journalIndexURL: str,
#         baseURL: str = "",
#         feedType: Literal["api", "atom", "rss"] = "rss",
#     ) -> None:
#         self.journalBaseName: str = baseName
#         self.journalBaseURL: str = baseURL

#         self.journalFeedType: Literal["api", "atom", "rss"] = feedType

#         self.journalIndexURL: str = journalIndexURL
#         self.journalIndexSoup: BeautifulSoup = BeautifulSoup()
#         self.journalIndexHTMLPath: Path = Path("html", self.journalBaseName + ".html")

#         self.subjournals: dict[str, str] = {}


#     def buildClass(self) -> str:
#         classNames: List[str] = list(self.subjournals.keys())
#         urls: List[str] = list(self.subjournals.values())

#         formattedClassNames: List[str] = list(map(_replaceText, classNames))

#         feedURL: str = f"{url[:-1]}.rss"

#         return f"""
#     class {className}(Journal):
#     def __init__(self)  ->  None:
#         self.name= "{name}"
#         self.url= "{url}"
#         self.feedType= "{feedType}"
#         self.feedURL= "{feedURL}"
#         self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
#         self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
#         self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

#     def entryDownloadURL(self, **kwargs)    ->  str:
#         if "entryDOI" in kwargs:
#             partialDOI: str = kwargs.get("entryDOI").split("/")[1]
#             return self.entryDownloadURLTemplate.substitute(partialDOI)
#         return ""
# """


# def main() -> None:
#     soup: BeautifulSoup = getRawNaturePortfolio()
#     nameHREFPairs: dict[str, str] = extractRelevantData(soup=soup)

#     data: str = ""

#     key: str
#     for key in nameHREFPairs.keys():
#         data += buildClass(name=key, link=nameHREFPairs[key])

#     print(data)


# if __name__ == "__main__":
#     main()
