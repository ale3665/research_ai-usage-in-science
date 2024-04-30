from datetime import datetime
from typing import List

from requests import Response, get

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


class Search:
    """
    Generic class for searching through mega journals

    This class is meant to be inherited by other related classes in order to
    facilitate searching through mega journals
    """

    def __init__(self) -> None:
        """
        __init__ Initalize the Search class

        Initalizes the Search class with standard headers
        """
        self.headers: dict[str, str] = {}

    def search(self, url: str) -> Response:
        """
        search Return the response of a search query to a website

        Given a URL, get that page's URL.

        :param url: The URL of the relevant page to get
        :type url: str
        :return: The Response object of that URL containing the HTML, status code, and header information
        :rtype: Response
        """
        resp: Response = get(url=url, headers=self.headers)
        return resp
