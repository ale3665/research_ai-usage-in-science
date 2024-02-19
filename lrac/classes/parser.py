from time import time
from typing import List

import feedparser
from feedparser.util import FeedParserDict
from pandas import DataFrame

from lrac.classes.journals import Journal


class Parser:
    def __init__(self) -> None:
        self.currentFeed: FeedParserDict | None = None
        self.currentFeedURL: str | None = None
        self.currentFeedBaseURL: str | None = None
        self.currentFeedName: str | None = None
        self.feedRetrievalTime: float | None = None
        self.currentDocumentTags: List[str] | None = None

    def clear(self) -> None:
        """
        Clear the current data captured by the FeedParser.
        """
        self.currentFeed = None
        self.currentFeedBaseURL = None
        self.currentFeedName = None
        self.currentFeedURL = None
        self.currentDocumentTags = None

    def getFeed(self, source: Journal) -> None:
        """
        Get the latest feed from a source
        """
        if self.currentFeedName is not source.name:
            self.currentFeedName = source.name
            self.currentFeedBaseURL = source.url
            self.currentFeedURL = source.rssURL
            self.currentFeed = feedparser.parse(url_file_stream_or_string=source.rssURL)
            self.feedRetrievalTime = time()
            self.currentDocumentTags = source.documentTags

    def parseFeed(self) -> DataFrame | None:
        """
        Parse the feed for all research articles and return a DataFrame with
        relevant article features.

        Research articles are identified by a journals documentTags attribute
        accessible via self.currentDocumentTags .
        """

        if self.currentFeed is None:
            return None

        data: dict[str, List[str]] = {
            "doi": [],
            "url": [],
            "title": [],
            "source": [],
            "updated": [],
        }

        entries: List[FeedParserDict] = self.currentFeed["entries"]

        entry: FeedParserDict
        for entry in entries:
            if entry["dc_type"] in self.currentDocumentTags:
                data["source"].extend([self.currentFeedName])
                data["title"].extend([entry["title"]])
                data["url"].extend([entry["link"]])
                data["doi"].extend([entry["prism_doi"]])
                data["updated"].extend([entry["updated"]])

        return DataFrame(data=data)
