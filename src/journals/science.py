from string import Template
from typing import List, Literal

from bs4 import BeautifulSoup, ResultSet, Tag
from pandas import DataFrame
from progress.bar import Bar
from requests import Response

from src.utils.search import DATA_STOR, Journal_ABC, Search, dfSchema


class Science(Journal_ABC):
    """
    Class to search through the Science mega journal

    This class implements the necessary methods to search through and paginate
    responses from the Science mega journal.
    """

    def __init__(self) -> None:
        """
        __init__ Initalize the Science class

        Initalizes the Science class with a set URL template
        """
        self.url: Template = Template(
            template="https://www.science.org/action/doSearch?AllField=${query}&ConceptID=505154&Earliest=[${year}0101+TO+${year}1231]&startPage=${page}&sortBy=Earliest&pageSize=100",
        )
        self.search: Search = Search()
        self.journal: str = "Science"

    def conductSearch(self, query: str, year: int) -> DataFrame:
        data: dict[str, List[str | int | bytes]] = DATA_STOR.copy()
        page: int = 0
        maxPage: int = 1

        with Bar(f"Conducting search for {query} in {year}...", max=1) as bar:
            while True:
                if page > maxPage - 1:
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

                if page == 0:
                    # Check to ensure that there exists pagination
                    paginationCheck: Literal[False] | int = self.identifyPagination(
                        resp=resp
                    )

                    if paginationCheck is not False:
                        maxPage = paginationCheck
                        bar.max = maxPage
                        bar.update()

                bar.next()
                page += 1

        return dfSchema(df=DataFrame(data=data)).df

    def identifyPagination(self, resp: Response) -> Literal[False] | int:
        maxPage: int = 1

        soup: BeautifulSoup = BeautifulSoup(
            markup=resp.content,
            features="lxml",
        )

        paginationBlock: ResultSet = soup.find_all(
            name="li",
            attrs={"class": "page-item"},
        )

        block: Tag
        for block in paginationBlock:
            try:
                page: int = int(block.text)
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
