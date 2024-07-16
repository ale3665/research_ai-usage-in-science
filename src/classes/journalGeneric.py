from abc import ABCMeta, abstractmethod
from typing import List

from bs4 import BeautifulSoup
from pandas import DataFrame


class Journal_ABC(metaclass=ABCMeta):
    """
    Journal_ABC _summary_

    _extended_summary_

    :param metaclass: _description_, defaults to ABCMeta
    :type metaclass: _type_, optional
    """

    @abstractmethod
    def searchJournal(self, query: str, year: int) -> DataFrame:

        pass

    @abstractmethod
    def extractPaperURLsFromSearchResult(self, respContent: str) -> List[str]:
        pass

    @abstractmethod
    def extractDOIFromPaper(self, url: str) -> str:
        pass

    @abstractmethod
    def extractTitleFromPaper(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def extractAbstractFromPaper(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def extractContentFromPaper(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def extractJournalTagsFromPaper(self, soup: BeautifulSoup) -> List[str]:
        pass
