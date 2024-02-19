from lrac.classes.journals import Journal, Science
import feedparser
from feedparser.util import FeedParserDict
from time import time
from pandas import DataFrame
from typing import List
from pprint import pprint as print

class Parser:
    def __init__(self)  ->  None:
        self.currentFeed: FeedParserDict | None = None
        self.currentFeedURL: str | None = None
        self.currentFeedBaseURL: str | None = None
        self.currentFeedName: str | None = None
        self.feedRetrievalTime: float | None = None
    
    def clear(self) ->  None:
        """
        Clear the current data captured by the FeedParser.
        """
        self.currentFeed = None
        self.currentFeedBaseURL = None
        self.currentFeedName = None
        self.currentFeedURL = None

    def getFeed(self, source: Journal)  ->  None:
        """
        Get the latest feed from a source
        """
        if self.currentFeedName is None:
            self.currentFeedName = source.name
            self.currentFeedBaseURL = source.url
            self.currentFeedURL = source.rssURL
            self.currentFeed = feedparser.parse(url_file_stream_or_string=source.rssURL)
            self.feedRetrievalTime = time()

    def parseFeed(self) ->  DataFrame | None:
        """
        Parse the feed for all research articles and return a DataFrame with
        their DOI, URL, Title, and Source information.

        Research articles are identified by a journals documentTags attribute.
        """

        if self.currentFeed is None:
            return None
        
        data: dict[str, List[str]] = {
                "doi": [],
                "url": [],
                "title": [],
                "source": [],
                }

        entries: List[FeedParserDict] = self.currentFeed["entries"]

        entry: FeedParserDict
        for entry in entries:
            # TODO: Replace this with a search against the classes documentTags
            # attribute
            if entry["dc_type"] == "Research Article":
                data["source"].extend([self.currentFeedName])
                data["title"].extend([entry["title"]])
                data["url"].extend([entry["link"]])
                data["doi"].extend([entry["prism_doi"]])

        return DataFrame(data=data)

s = Science()
fp = Parser()

fp.getFeed(source=s)
df = fp.parseFeed()
print(df)
print(df["url"].to_list())
