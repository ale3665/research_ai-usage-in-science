import pickle
from itertools import product
from math import ceil
from string import Template
from typing import List, Literal

import pandas
from pandas import DataFrame
from progress.bar import Bar
from requests import Response

from aius.search import DATA_STOR, RELEVANT_YEARS, SEARCH_QUERIES, Journal_ABC, dfSchema
from aius.search.search import Search


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

        json: dict = resp.json()

        documentsFound: int = json["searchResults"]["numFound"]

        if documentsFound >= 100:
            maxPage = ceil(documentsFound / 100)

        return maxPage


def main() -> None:
    data: List[DataFrame] = []

    plos: PLOS = PLOS()

    for pair in product(SEARCH_QUERIES, RELEVANT_YEARS):
        df: DataFrame = plos.conductSearch(query=pair[0], year=pair[1])
        data.append(df)

    df: DataFrame = pandas.concat(objs=data, ignore_index=True)
    df.drop_duplicates(
        subset=["url"],
        keep="first",
        inplace=True,
        ignore_index=True,
    )

    with open(file="plos.pickle", mode="wb") as pickleFile:
        pickle.dump(obj=df, file=pickleFile)
        pickleFile.close()


if __name__ == "__main__":
    main()


# def getJSON(url: str) -> dict:
#     response: Response = get(url=url)
#     return response.json()


# def main() -> None:
#     dataDirectory: Path = resolvePath(path=Path("../../data/json/plos"))

#     urlTemplate: Template = Template(
#         template="https://journals.plos.org/plosone/dynamicSearch?filterStartDate=${year}-01-01&filterEndDate=${year}-12-31&resultsPerPage=60&q=${query}&sortOrder=DATE_NEWEST_FIRST&page=${page}&ilterArticleTypes=Research Article"
#     )
#     queries: List[str] = [
#         r'"Deep Learning"',
#         r'"Deep Neural Network"',
#         r'"Hugging Face"',
#         r'"HuggingFace"',
#         r'"Pre-Trained Model"',
#     ]
#     years: List[int] = list(range(2015, datetime.now().year + 1))

#     query: str
#     year: int
#     for query in queries:
#         for year in years:
#             formattedQuery: str = query.replace('"', "")
#             with Spinner(f"Downloading {formattedQuery} {year} data...") as spinner:
#                 pagination: int = 1
#                 while True:
#                     url: str = urlTemplate.substitute(
#                         year=year,
#                         query=query,
#                         page=pagination,
#                     )
#                     json: dict = getJSON(url=url)

#                     hitCount: int
#                     try:
#                         hitCount = json["searchFilters"]["article_type"][
#                             "inactiveFilterItems"
#                         ][0]["numberOfHits"]
#                     except KeyError:
#                         hitCount = 60

#                     filename: Path
#                     if pagination == 1:
#                         filename = Path(f"{formattedQuery} {year}.json")
#                     else:
#                         filename = Path(f"{formattedQuery} {year} {pagination}.json")

#                     with open(file=Path(dataDirectory, filename), mode="w") as jsonFile:
#                         dump(obj=json, fp=jsonFile, indent=4)
#                         jsonFile.close()

#                     pages: int = ceil(hitCount / 60)

#                     if pagination == pages:
#                         spinner.next()
#                         break
#                     else:
#                         pagination += 1
#                         spinner.next()


# if __name__ == "__main__":
#     main()
