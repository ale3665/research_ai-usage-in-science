from json import dump, load
from math import ceil
from os.path import isfile
from typing import List

from pandas import DataFrame
from requests import Response, get


def getJSONResponse() -> dict:
    filename: str = "searchResponse_plos.json"

    json: dict
    if isfile(path=filename):
        with open(file="searchResponse_plos.json", mode="r") as jsonFile:
            json = load(fp=jsonFile)
            jsonFile.close()
    else:
        # Query: "Deep Learning"
        # Year: 2016
        # Page: 1
        url: str = (
            "https://journals.plos.org/plosone/dynamicSearch?filterStartDate=2016-01-01&filterEndDate=2016-12-31&resultsPerPage=100&q=%E2%80%9DDeep%20Learning%E2%80%9D&sortOrder=DATE_NEWEST_FIRST&page=74&filterArticleTypes=Research%20Article"  # noqa: E501
        )

        resp: Response = get(url=url, timeout=60)
        json = resp.json()

        with open(file="searchResponse_plos.json", mode="w") as jsonFile:
            dump(obj=json, fp=jsonFile)
            jsonFile.close()

    return json


def searchResultStats(searchResults: dict[str, dict | List]) -> None:
    print("Total documents found:", searchResults["numFound"])
    print("Documents per page:", len(searchResults["docs"]))
    print("Number of pages:", ceil(searchResults["numFound"] / 100))


def sampleDocs(docs: List[dict[str, str | dict]]) -> DataFrame:
    df: DataFrame = DataFrame(data=docs)
    df["id"] = df["id"].apply(lambda x: f"https://doi.org/{x}")

    return df.sample(n=30, replace=False, random_state=42, ignore_index=True)


def main() -> None:
    json: dict = getJSONResponse()

    searchResults: dict[str, dict | List] = json["searchResults"]
    searchResultStats(searchResults=searchResults)

    docs: List[dict[str, str]] = searchResults["docs"]

    sampleDF: DataFrame = sampleDocs(docs=docs)

    print(sampleDF)


if __name__ == "__main__":
    main()
