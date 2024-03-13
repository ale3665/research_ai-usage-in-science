from datetime import datetime
from time import mktime
from typing import List

import feedparser
from feedparser import FeedParserDict
from pandas import DataFrame


def getRSSFeed(feedURL: str) -> FeedParserDict:
    return feedparser.parse(url_file_stream_or_string=feedURL)


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
        data["updated"].append(datetime.fromtimestamp(mktime(entry["updated_parsed"])))
        data["added"].append(datetime.now())

    return DataFrame(data=data)
