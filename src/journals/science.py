from string import Template
from typing import List
from urllib.parse import quote_plus

from pandas import DataFrame


class Science:
    def __init__(self) -> None:
        self.journalName: str = "Science"
        self.searchURLTemplate: Template = Template(
            "https://www.science.org/action/doSearch?AllField=${query}&ConceptID=505154&ConceptID=505172&AfterYear=${year}&BeforeYear=${year}&queryID=8%2F7249304983&sortBy=Earliest"  # noqa: E501
        )

    def generateURLs(
        self,
        years: List[int],
        queries: List[str],
    ) -> DataFrame:
        json: dict[str, List[str]] = {}

        query: str
        for query in queries:
            key = query.replace('"', "")
            json[key] = []

            year: int
            for year in years:
                json[key].append(
                    self.searchURLTemplate.substitute(
                        year=year,
                        query=quote_plus(
                            string=query,
                        ),
                    )
                )

        return DataFrame(data=json)
