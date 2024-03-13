from os.path import isfile
from pathlib import Path

from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, get

NATURE_BASE_URL: str = "https://www.nature.com"
NATURE_BASE_TITLE: str = "Nature"


def getRawNaturePortfolio() -> BeautifulSoup:
    natureHTMLFile: Path = Path("_natureSiteIndex.html")

    if isfile(natureHTMLFile):
        return BeautifulSoup(markup=open(natureHTMLFile), features="lxml")

    else:
        resp: Response = get(url=f"{NATURE_BASE_URL}/siteindex")

        with open(natureHTMLFile, "w") as htmlFile:
            htmlFile.write(resp.content.__str__())
        return BeautifulSoup(markup=resp.content, features="lxml")


def extractRelevantData(soup: BeautifulSoup) -> dict[str, str]:
    data: dict[str, str] = {}

    searchQuery: dict[str, str] = {"class": "block pt10 pb10 equalize-line-height"}
    links: ResultSet = soup.find_all(name="a", attrs=searchQuery)

    link: Tag
    for link in links:
        data[f"{NATURE_BASE_TITLE} {link.text}"] = link.get(key="href")

    return data


def buildClass(name: str, link: str) -> str:
    className: str = (
        name.replace(" ", "")
        .replace("&", "And")
        .replace("-", "")
        .replace(":", "")
        .replace("'", "")
        .replace(r"\xe2\x80\x94", "")
    )
    url: str = NATURE_BASE_URL + link
    feedType: str = "rss"
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
        print(f'"{key}":"{NATURE_BASE_URL}{nameHREFPairs[key][:-1]}.rss",')
        data += buildClass(name=key, link=nameHREFPairs[key])

    # print(data)


if __name__ == "__main__":
    main()
