from math import ceil
from string import Template
from typing import List

from pandas import DataFrame
from progress.bar import Bar
from requests import Response

from src.classes import SEARCH_RESULTS_STOR, SearchResultDataFrameSchema
from src.classes.journalGeneric import Journal_ABC


class PLOS(Journal_ABC):
    def __init__(self) -> None:
        self.journalName: str = "PLOS"
        self.searchURLTemplate: Template = Template(
            template="https://journals.plos.org/plosone/dynamicSearch?filterStartDate=${year}-01-01&filterEndDate=${year}-12-31&resultsPerPage=100&q=${query}&sortOrder=DATE_NEWEST_FIRST&page=${page}&filterArticleTypes=Research Article"  # noqa: E501
        )

    def search(self, query: str, year: int) -> DataFrame:
        """
        search _summary_

        _extended_summary_

        :param query: _description_
        :type query: str
        :param year: _description_
        :type year: int
        :return: _description_
        :rtype: DataFrame
        """
        data: dict[str, List[str | int | bytes]] = SEARCH_RESULTS_STOR.copy()
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
                    json: dict[str, str] = resp.json()

                    documentsFound: int = json["searchResults"]["numFound"]

                    if documentsFound >= 100:
                        maxPage: int = ceil(documentsFound / 100)
                        bar.max = maxPage
                        bar.update()

                bar.next()
                page += 1

        return SearchResultDataFrameSchema(df=DataFrame(data=data)).df

    def extractPaperURLs(self) -> None:
        pass

    def downloadPapers(self) -> None:
        pass

    def extractDOIFromPaper(self) -> None:
        pass

    def extractTitleFromPaper(self) -> None:
        pass

    def extractAbstractFromPaper(self) -> None:
        pass

    def extractContentFromPaper(self) -> None:
        pass

    def createZettel(self) -> None:
        pass
