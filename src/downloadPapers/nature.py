from typing import List

from bs4 import BeautifulSoup, ResultSet, Tag

from src.downloadPapers import Journal_ABC


class Nature(Journal_ABC):
    def __init__(self) -> None:
        self.baseURL: str = "https://www.nature.com"

    def getPaperURLs(self, html: str) -> List[str]:
        data: List[str] = []

        soup: BeautifulSoup = BeautifulSoup(
            markup=html,
            features="lxml",
        )
        urls: ResultSet = soup.find_all(
            name="a",
            attrs={"class": "c-card__link"},
        )

        url: Tag
        for url in urls:
            completeURL: str = self.baseURL + url.get(key="href")
            data.append(completeURL)

        return data
