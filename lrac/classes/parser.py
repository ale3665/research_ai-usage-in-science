from datetime import datetime
from json import dump, load
from os import mkdir
from pathlib import Path
from time import mktime, time
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
        self.currentRSSFilepath: Path | None = None

    def clear(self) -> None:
        """
        Clear the current data captured by the FeedParser.
        """
        self.currentFeed = None
        self.currentFeedBaseURL = None
        self.currentFeedName = None
        self.currentFeedURL = None
        self.currentDocumentTags = None
        self.currentRSSFilepath = None

    def getFeed(self, source: Journal, rssStore: Path) -> None:
        """
        Get the latest feed from a source and save the feed to disk
        """
        if self.currentFeedName is not source.name:
            self.feedRetrievalTime = time()

            self.currentRSSFilepath = Path(
                rssStore, source.name + f"_{self.feedRetrievalTime}.json"
            )
            self.currentFeedName = source.name
            self.currentFeedBaseURL = source.url
            self.currentFeedURL = source.rssURL
            self.currentDocumentTags = source.documentTags

            self.currentFeed = feedparser.parse(url_file_stream_or_string=source.rssURL)

            try:
                mkdir(path=rssStore)
            except FileExistsError:
                pass

            with open(file=self.currentRSSFilepath, mode="w") as jsonFeed:
                dump(
                    obj=self.currentFeed,
                    fp=jsonFeed,
                    indent=4,
                )
                jsonFeed.close()

    def parseFeed(self, pdfStore: Path) -> DataFrame | None:
        """
        Parse the feed for all research articles and return a DataFrame with
        relevant article features.

        Research articles are identified by a journals documentTags attribute
        accessible via self.currentDocumentTags .
        """

        if self.currentFeed is None:
            return None

        data: dict[str, List[str | datetime]] = {
            "doi": [],
            "url": [],
            "title": [],
            "source": [],
            "updated": [],
            "pdfFilepath": [],
            "feedFilepath": [],
        }

        entries: List[FeedParserDict] = self.currentFeed["entries"]

        entry: FeedParserDict
        for entry in entries:
            if entry["dc_type"] in self.currentDocumentTags:
                data["feedFilepath"].extend([self.currentRSSFilepath.__str__()])
                data["source"].extend([self.currentFeedName])
                data["title"].extend([entry["title"]])
                data["url"].extend([entry["link"]])
                data["doi"].extend([entry["prism_doi"]])
                data["pdfFilepath"].extend(
                    [
                        Path(
                            pdfStore, entry["prism_doi"].replace("/", "_") + ".pdf"
                        ).__str__()
                    ]
                )

                parsedTime: float = mktime(entry["updated_parsed"])
                datetimeObject: datetime = datetime.fromtimestamp(parsedTime)

                data["updated"].extend([datetimeObject])
        return DataFrame(data=data)
