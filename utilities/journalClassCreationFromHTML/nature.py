from os.path import isfile
from pathlib import Path
from typing import List

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


def main() -> None:
    soup: BeautifulSoup = getRawNaturePortfolio()
    nameHREFPairs: dict[str, str] = extractRelevantData(soup=soup)

    from pprint import pprint as print

    print(nameHREFPairs)


if __name__ == "__main__":
    main()
