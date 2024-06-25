from datetime import datetime
from time import mktime
from typing import List

from bs4 import BeautifulSoup, ResultSet, Tag
from feedparser import FeedParserDict
from pandas import DataFrame
from requests import Response, get

DOI_SUFFIX: str = "10.1038"


def getSoup(url: str) -> BeautifulSoup:
    resp: Response = get(url=url, timeout=60)
    return BeautifulSoup(markup=resp.content, features="lxml")


def extractArticleFields(soup: BeautifulSoup, journal: str) -> List[Tag]:
    articles: ResultSet = soup.find_all(
        name="article",
        attrs={
            "class": "u-full-height c-card c-card--flush",
        },
    )

    article: Tag
    for article in articles:
        journal: str = journal
        title: str = article.find(
            name="h3", attrs={"class": "c-card__title"}
        ).getText(strip=True)
        url: str = article.find(
            name="a", attrs={"class": "c-card__link u-link-inherit"}
        ).get(key="href")
        doi: str = DOI_SUFFIX + "/" + url.split(sep="/")[-1]
        updatedTime: str = article.find(
            name="time",
            attrs={
                "class": "c-meta__item c-meta__item--block-at-lg",
            },
        ).get("datetime")

        print(updatedTime)


def parseFeed(feed: FeedParserDict) -> DataFrame:
    data: dict[str, List[str | datetime]] = {
        "doi": [],
        "url": [],
        "title": [],
        "journal": [],
        "updated": [],
        "added": [],
    }

    entries: List[dict] = feed["entries"]

    entry: dict
    for entry in entries:
        data["doi"].append(entry["prism_doi"])
        data["url"].append(entry["prism_url"])
        data["title"].append(entry["title"])
        data["journal"].append(entry["prism_publicationname"])
        data["updated"].append(
            datetime.fromtimestamp(mktime(entry["updated_parsed"]))
        )
        data["added"].append(datetime.now())

    return DataFrame(data=data)


s = getSoup(url="https://www.nature.com/aps/research-articles")

extractArticleFields(soup=s, journal="s")
