from os.path import isfile
from pathlib import Path

from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, get

NATURE_BASE_URL: str = "https://www.nature.com"
NATURE_BASE_TITLE: str = "Nature"


def getRawNaturePortfolio() -> BeautifulSoup:
    natureHTMLFile: Path = Path("natureSiteIndex.html")

    if isfile(natureHTMLFile):
        return BeautifulSoup(markup=open(natureHTMLFile), features="lxml")

    else:
        resp: Response = get(url=f"{NATURE_BASE_URL}/siteindex")

        with open("natureSiteIndex.html", "w") as htmlFile:
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
class {className}:
    def __init__(self)  ->  None:
        self.name = "{name}"
        self.url = "{url}"
        self.feedType = "{feedType}"
        self.feedURL = "{feedURL}"
        self.entryTags = []
        self.entryTagKeys = []
        self.endtryDownloadURLTemplate = ""

    def entryDownloadURL(self, **kwargs)    ->  str:
        ...
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
