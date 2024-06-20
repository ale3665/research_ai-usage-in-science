from abc import ABCMeta, abstractmethod
from typing import List

from bs4 import BeautifulSoup, ResultSet, Tag


class Journal_ABC(metaclass=ABCMeta):
    @abstractmethod
    def getPaperURLs(self, html: str) -> List[str]:
        data: List[str] = []

        soup: BeautifulSoup = BeautifulSoup(
            markup=html,
            features="lxml",
        )
        urls: ResultSet = soup.find_all(name="a", attrs={"class": "c-card__link"})

        url: Tag
        for url in urls:
            completeURL: str = self.baseURL + url.get(key="href")
            data.append(completeURL)

        return data
