from json import loads
from typing import List

from aius.downloadPapers import Journal_ABC


class PLOS(Journal_ABC):
    def __init__(self) -> None:
        self.baseURL: str = "https://journals.plos.org/plosone/article?id="

    def getPaperURLs(self, html: str) -> List[str]:
        data: List[str] = []

        json: dict = loads(s=html)
        searchResults: dict = json["searchResults"]
        docs: List[dict] = searchResults["docs"]

        doc: dict
        for doc in docs:
            data.append(self.baseURL + doc["id"])

        return data
