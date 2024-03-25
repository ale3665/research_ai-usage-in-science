from datetime import datetime
from json import dump
from math import ceil
from pathlib import Path
from string import Template
from typing import List

from progress.spinner import Spinner
from pyfs import resolvePath
from requests import Response, get


def getJSON(url: str) -> dict:
    response: Response = get(url=url)
    return response.json()


def main() -> None:
    dataDirectory: Path = resolvePath(path=Path("../../data/json/plos"))

    urlTemplate: Template = Template(
        template="https://journals.plos.org/plosone/dynamicSearch?filterStartDate=${year}-01-01&filterEndDate=${year}-12-31&resultsPerPage=60&q=${query}&sortOrder=DATE_NEWEST_FIRST&page=${page}&ilterArticleTypes=Research Article"
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
            formattedQuery: str = query.replace('"', "")
            with Spinner(f"Downloading {formattedQuery} {year} data...") as spinner:
                pagination: int = 1
                while True:
                    url: str = urlTemplate.substitute(
                        year=year,
                        query=query,
                        page=pagination,
                    )
                    json: dict = getJSON(url=url)

                    hitCount: int
                    try:
                        hitCount = json["searchFilters"]["article_type"][
                            "inactiveFilterItems"
                        ][0]["numberOfHits"]
                    except KeyError:
                        hitCount = 60

                    filename: Path
                    if pagination == 1:
                        filename = Path(f"{formattedQuery} {year}.json")
                    else:
                        filename = Path(f"{formattedQuery} {year} {pagination}.json")

                    with open(file=Path(dataDirectory, filename), mode="w") as jsonFile:
                        dump(obj=json, fp=jsonFile, indent=4)
                        jsonFile.close()

                    pages: int = ceil(hitCount / 60)

                    if pagination == pages:
                        spinner.next()
                        break
                    else:
                        pagination += 1
                        spinner.next()


if __name__ == "__main__":
    main()
