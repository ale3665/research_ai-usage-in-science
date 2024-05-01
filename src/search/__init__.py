from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Literal

from pandas import DataFrame
from requests import Response
from typedframe import TypedDataFrame

SEARCH_QUERIES: List[str] = [
    r'"Deep Learning"',
    r'"Deep Neural Network"',
    r'"Hugging Face"',
    r'"HuggingFace"',
    r'"Model Checkpoint"',
    r'"Model Weights"',
    r'"Pre-Trained Model"',
]

RELEVANT_YEARS: List[int] = list(range(2015, datetime.now().year + 1))

DATA_STOR: dict[str, List[str | int | bytes]] = {
    "year": [],
    "query": [],
    "page": [],
    "url": [],
    "status_code": [],
    "html": [],
}


class dfSchema(TypedDataFrame):
    schema: dict = {
        "year": int,
        "query": str,
        "page": int,
        "url": str,
        "status_code": int,
        "html": str,
    }


class Journal_ABC(metaclass=ABCMeta):
    @abstractmethod()
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

    @abstractmethod()
    def identifyPagination(self, resp: Response) -> Literal[False] | int:
        """
        identifyPagination Identify if a web page has pagination enabled

        Given a response object of an HTTP GET request, identify if that page has pagination enabled.

        :param resp: Response object of an HTTP GET request
        :type resp: Response
        :return: False if disabled, or an integer representing the number of pages availible for pagination
        :rtype: Literal[False] | int
        """
        ...
