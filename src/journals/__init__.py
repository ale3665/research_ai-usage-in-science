from abc import ABCMeta, abstractmethod
from typing import List, Literal

from bs4 import BeautifulSoup, ResultSet, Tag
from pandas import DataFrame
from requests import Response


class Journal_ABC(metaclass=ABCMeta):
    @abstractmethod
    def conductSearch(self, query: str, year: int) -> DataFrame:
        """
        conductSearch Given a search query, year, and page, search for documents

        :param query: The search query to search for
        :type query: str
        :param year: Limits the query to a given year
        :type year: int
        :return: A Pandas DataFrame of responses for a given search query in a specific year
        :rtype: DataFrame[Response]
        """
        ...

    @abstractmethod
    def identifyPaginationOfSearchResults(self, resp: Response) -> Literal[False] | int:
        """
        identifyPagination Identify if a web page has pagination enabled

        Given a response object of an HTTP GET request, identify if that page has pagination enabled.

        :param resp: Response object of an HTTP GET request
        :type resp: Response
        :return: False if disabled, or an integer representing the number of pages availible for pagination
        :rtype: Literal[False] | int
        """
        ...

    @abstractmethod
    def getPaperURLsFromSearchResults(self, html: str) -> List[str]:
        """
        getPaperURLs Return the URLs of papers returned from a search pages HTML

        :param html: Search result HTML
        :type html: str
        :return: A list of URLs within the search result HTML
        :rtype: List[str]
        """
        ...
