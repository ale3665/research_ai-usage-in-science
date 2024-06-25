from math import ceil
from string import Template
from typing import List, Literal

from pandas import DataFrame
from progress.bar import Bar
from requests import Response

from src.search import DATA_STOR, RELEVANT_YEARS, SEARCH_QUERIES, Journal_ABC, dfSchema
from src.search.search import Search


class PLOS(Journal_ABC):
    """
    Class to search through the PLOS mega journal

    This class implements the necessary methods to search through and paginate
    responses from the PLOS mega journal.
    """

    def __init__(self) -> None:
        """
        __init__ Initalize the PLOS class

        Initalizes the PLOS class with a set URL template
        """
        self.url: Template = Template(
            template="https://journals.plos.org/plosone/dynamicSearch?filterStartDate=${year}-01-01&filterEndDate=${year}-12-31&resultsPerPage=100&q=${query}&sortOrder=DATE_NEWEST_FIRST&page=${page}&filterArticleTypes=Research Article"
        )
        self.search: Search = Search()
        self.journal: str = "PLOS"

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

    def identifyPaginationOfSearchResults(self, resp: Response) -> Literal[False] | int:
        maxPage: int = 1

        json: dict = resp.json()

        documentsFound: int = json["searchResults"]["numFound"]

        if documentsFound >= 100:
            maxPage = ceil(documentsFound / 100)

        return maxPage
