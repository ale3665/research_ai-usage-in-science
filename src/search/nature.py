import pickle
from itertools import product
from string import Template
from typing import List, Literal

import pandas
from bs4 import BeautifulSoup, ResultSet, Tag
from pandas import DataFrame
from progress.bar import Bar
from requests import Response

from src.search import DATA_STOR, RELEVANT_YEARS, SEARCH_QUERIES, Journal_ABC, dfSchema
from src.search.search import Search


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
            template="https://www.nature.com/search?q=${query}&order=date_desc&article_type=research&date_range=${year}-${year}&page=${page}"
        )
        self.search: Search = Search()

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
    data: List[DataFrame] = []

    nature: Nature = Nature()

    for pair in product(SEARCH_QUERIES, RELEVANT_YEARS):
        df: DataFrame = nature.conductSearch(query=pair[0], year=pair[1])
        data.append(df)

    df: DataFrame = pandas.concat(objs=data, ignore_index=True)
    df.drop_duplicates(
        subset=["url"],
        keep="first",
        inplace=True,
        ignore_index=True,
    )

    with open(file="nature.pickle", mode="wb") as pickleFile:
        pickle.dump(obj=df, file=pickleFile)
        pickleFile.close()


if __name__ == "__main__":
    main()
