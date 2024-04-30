from datetime import datetime
from string import Template
from typing import List, Literal
from webbrowser import open

from bs4 import BeautifulSoup, ResultSet, Tag
from progress.bar import Bar
from requests import Response

from src.search import RELEVANT_YEARS, SEARCH_QUERIES, Search


class Nature(Search):
    """
    Class to search through the Nature mega journal

    This class implements the necessary methods to search through and paginate
    responses from the Nature mega journal.
    """

    def __init__(self) -> None:
        """
        __init__ Initalize the Nature class

        Initalizes the Nature class with a set URL template
        """
        self.url: Template = Template(
            template="https://www.nature.com/search?q=${query}&order=date_desc&article_type=research&date_range=${year}-${year}&page=${page}"
        )
        super().__init__()

    def conductSearch(self, query: str, year: int) -> List[Response]:
        """
        search Given a search query, year, and page, search for documents

        :param query: The search query to search for
        :type query: str
        :param year: Limits the query to a given year
        :type year: int
        :return: A list of responses containing the search responses for a given year
        :rtype: List[Response]
        """
        data: List[Response] = []
        page: int = 1
        maxPage: int = 1

        with Bar(f"Conducting search for {query} in {year}...", max=1) as bar:
            while True:
                url: str = self.url.substitute(
                    query=query,
                    year=year,
                    page=page,
                )

                resp: Response = self.search(url=url)
                data.append(resp)

                if page == 1:
                    # Check to ensure that there exists pagination
                    paginationCheck: Literal[False] | int = self.identifyPagination(
                        resp=resp
                    )

                    if paginationCheck is False:
                        # Do nothing
                        pass
                    else:
                        maxPage = paginationCheck
                        bar.max = maxPage
                        bar.update()

                bar.next()
                if page == maxPage:
                    break
                else:
                    page += 1

        return data

    def identifyPagination(self, resp: Response) -> Literal[False] | int:
        maxPage: int = 1

        soup: BeautifulSoup = BeautifulSoup(
            markup=resp.content,
            features="lxml",
        )

        paginationBlock: ResultSet = soup.find_all(
            name="li",
            attrs={"class": "c-pagination__item"},
        )

        block: Tag
        for block in paginationBlock:
            try:
                page: int = int(block.get(key="data-page"))
            except ValueError:
                continue
            except TypeError:
                continue

            if page > maxPage:
                maxPage = page

        if maxPage <= 1:
            return False
        else:
            return maxPage


def main() -> None:
    urlTemplate: Template = Template(
        template="https://www.nature.com/search?q=${query}&order=date_desc&article_type=research&date_range=${year}-${year}"
    )
    queries: List[str] = [
        r'"Deep Learning"',
        r'"Deep Neural Network"',
        r'"Hugging Face"',
        r'"HuggingFace"',
        r'"Pre-Trained Model"',
    ]
    years: List[int] = list(range(2015, datetime.now().year + 1))

    query: str
    year: int
    for query in queries:
        for year in years:
            open(url=urlTemplate.substitute(query=query, year=year))


if __name__ == "__main__":
    n = Nature()
    n.conductSearch(query=r'"Deep Neural Network"', year=2024)
