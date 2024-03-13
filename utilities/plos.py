from os.path import isfile
from pathlib import Path

from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, get

PLOS_BASE_TITLE: str = "PLOS"


def getRawPlosPortfolio() -> BeautifulSoup:
    plosHTMLFile: Path = Path("plosJournalOptions.html")

    if isfile(plosHTMLFile):
        return BeautifulSoup(markup=open(plosHTMLFile), features="lxml")

    else:
        resp: Response = get(url="https://plos.org/your-journal-options/")

        with open(plosHTMLFile, "w") as htmlFile:
            htmlFile.write(resp.content.__str__())
        return BeautifulSoup(markup=resp.content, features="lxml")


def extractRelevantData(soup: BeautifulSoup) -> dict[str, str]:
    data: dict[str, str] = {}

    searchQuery: dict[str, str] = {
        "class": "journal-selector__list-item-background-image"
    }
    links: ResultSet = soup.find_all(name="a", attrs=searchQuery)

    link: Tag
    for link in links:
        data[f"{PLOS_BASE_TITLE} {link.text}"] = link.get(key="href")

    return data


def buildClass(name: str, link: str) -> str:
    className: str = (
        name.strip()
        .replace(" ", "")
        .replace(r"\n", "")
        .replace("&", "And")
        .replace("-", "")
        .replace(":", "")
        .replace("'", "")
        .replace(r"\xe2\x80\x94", "")
    )
    nameFormatted: str = name.strip().replace("  ", "").replace(r"\n", "")
    url: str = link
    feedType: str = "atom"
    feedURL: str = f"{url[:-1]}.rss"

    return f"""
class {className}(Journal):
    def __init__(self)  ->  None:
        self.name= "{nameFormatted}"
        self.url= "{url}"
        self.feedType= "{feedType}"
        self.feedURL= "{feedURL}"
        self.entryTags = PLOS_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = PLOS_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = PLOS_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs)    ->  str:
        if "entryDOI" in kwargs:
            partialDOI: str = kwargs.get("entryDOI").split("/")[1]
            return self.entryDownloadURLTemplate.substitute(partialDOI)
        return ""
"""


def main() -> None:
    soup: BeautifulSoup = getRawPlosPortfolio()
    nameHREFPairs: dict[str, str] = extractRelevantData(soup=soup)

    data: str = ""

    key: str
    for key in nameHREFPairs.keys():
        print(f'"{key.strip().replace("  ", "")}":"{nameHREFPairs[key]}",')
        data += buildClass(name=key, link=nameHREFPairs[key])

    # print(data)


if __name__ == "__main__":
    main()
