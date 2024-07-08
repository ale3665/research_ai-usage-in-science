from string import Template
from typing import List, Literal

from bs4 import BeautifulSoup, ResultSet, Tag
from pandas import DataFrame
from progress.bar import Bar
from requests import Response

from src.journals import Journal_ABC
from src.utils.search import DATA_STOR, Search, dfSchema


class Nature(Journal_ABC):
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
            template="https://www.nature.com/search?q=${query}&order=date_desc&article_type=research&date_range=${year}-${year}&page=${page}"  # noqa: E501
        )
        self.search: Search = Search()
        self.journal: str = "Nature"

    def conductSearch(self, query: str, year: int) -> DataFrame:
        data: dict[str, List[str | int | bytes]] = DATA_STOR.copy()
        page: int = 1
        maxPage: int = 1

        with Bar(f"Conducting search for {query} in {year}...", max=1) as bar:
            while True:
                if page > maxPage:
                    break

                url: str = self.url.substitute(
                    query=query,
                    year=year,
                    page=page,
                )

                resp: Response = self.search.search(url=url)

                data["year"].append(year)
                data["query"].append(query)
                data["page"].append(page)
                data["url"].append(url)
                data["status_code"].append(resp.status_code)
                data["html"].append(resp.content.decode(errors="ignore"))
                data["journal"].append(self.journal)

                if page == 1:
                    # Check to ensure that there exists pagination
                    paginationCheck: Literal[False] | int = (
                        self.identifyPaginationOfSearchResults(resp=resp)
                    )

                    if paginationCheck is not False:
                        maxPage = paginationCheck
                        bar.max = maxPage
                        bar.update()

                bar.next()
                page += 1

        return dfSchema(df=DataFrame(data=data)).df

    def identifyPaginationOfSearchResults(
        self,
        resp: Response,
    ) -> Literal[False] | int:
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

    def getPaperURLsFromSearchResults(self, html: str) -> List[str]:
        return []
