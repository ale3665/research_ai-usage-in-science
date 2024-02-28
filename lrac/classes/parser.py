from datetime import datetime
from json import dump
from pathlib import Path
from time import mktime, time
from typing import Any, List

import feedparser
from feedparser.util import FeedParserDict
from pandas import DataFrame

from lrac.classes.journals import Journal
from lrac.utils.fs import createDirectory


class Parser:
    def __init__(self) -> None:
        self.currentSource: Journal = None

        self.currentFeedRetrievalTime: float | None = None
        self.currentFeedFilepath: Path | None = None
        self.currentFeedDict: FeedParserDict | None = None

    def getFeed(self, source: Journal, feedStore: Path) -> None:
        """
        Get the latest feed from a source and save the feed to disk
        """
        try:
            nameTest: bool = self.currentSource.name != source.name
        except AttributeError:
            nameTest: bool = True

        if nameTest:
            self.currentSource = source
            self.currentFeedRetrievalTime = time()
            self.currentFeedDict = feedparser.parse(
                url_file_stream_or_string=self.currentSource.feedURL,
            )
            self.currentFeedFilepath = Path(
                feedStore,
                source.name + f"_{self.currentFeedRetrievalTime}.json",
            )

            createDirectory(directory=feedStore)

            with open(file=self.currentFeedFilepath, mode="w") as jsonFeed:
                dump(
                    obj=self.currentFeedDict,
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

        if self.currentFeedDict is None:
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

        def _parseRSSFeed(
            feedEntries: List[FeedParserDict],
        ) -> None:
            entry: FeedParserDict
            for entry in feedEntries:
                if self.currentSource.entryTagKeys is not None:
                    releventEntryTagKeys: set = set(entry.keys()).intersection(
                        self.currentSource.entryTagKeys
                    )
                    # This conditional first creates a set of all keys from
                    # the current feed (x).
                    # It then intersects x with the set of all supported
                    # entry keys for that particular journal (y) resulting
                    # in a new set (z).
                    if len(releventEntryTagKeys) > 0:
                        # If z > 0, then there is at least one item in the feed
                        # that is of interest to parse.
                        # Else, the loop continues
                        key: str
                        for key in releventEntryTagKeys:
                            if entry[key] in self.currentSource.entryTags:
                                parsedTime: float = mktime(entry["updated_parsed"])
                                parsedDatetimeObject: datetime = datetime.fromtimestamp(
                                    parsedTime
                                )

                                data["doi"].extend([entry["prism_doi"]])
                                data["url"].extend([entry["link"]])
                                data["title"].extend([entry["title"]])
                                data["source"].extend([self.currentSource.name])
                                data["updated"].extend([parsedDatetimeObject])
                                data["pdfFilepath"].extend(
                                    [
                                        Path(
                                            pdfStore,
                                            entry["prism_doi"].replace("/", "_")
                                            + ".pdf",
                                        ).__str__()
                                    ]
                                )
                                data["feedFilepath"].extend(
                                    [self.currentFeedFilepath.__str__()]
                                )
                    else:
                        continue

        entries: List[FeedParserDict] = self.currentFeedDict["entries"]

        match self.currentSource.feedType:
            case "api":
                pass
            case "atom":
                pass
            case "rss":
                _parseRSSFeed(feedEntries=entries)

        return DataFrame(data=data)
