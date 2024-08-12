from os.path import isfile
from typing import List

import pandas
from pandas import DataFrame
from progress.bar import Bar
from requests import Response, get

RANDOM_SEED: int = 42


def getJSONResponse() -> DataFrame:
    filename: str = "searchResponse_plos.json"

    json: DataFrame
    if isfile(path=filename):
        json = pandas.read_json(path_or_buf=filename)

    else:
        dfs: List[DataFrame] = []

        with Bar("Getting JSON responses...", max=75) as bar:
            page: int
            for page in range(1, 76):
                # Query: "Deep Learning"
                # Year: 2016
                # Page: 1
                # Max page: 75
                url: str = (
                    f"https://journals.plos.org/plosone/dynamicSearch?filterStartDate=2016-01-01&filterEndDate=2016-12-31&resultsPerPage=100&q=%E2%80%9DDeep%20Learning%E2%80%9D&sortOrder=DATE_NEWEST_FIRST&page={page}&filterArticleTypes=Research%20Article"  # noqa: E501
                )

                resp: Response = get(url=url, timeout=60)
                json = resp.json()

                dfs.append(DataFrame(data=json["searchResults"]["docs"]))

                bar.next()

        json = pandas.concat(objs=dfs, ignore_index=True)
        json["id"] = json["id"].apply(lambda x: f"https://doi.org/{x}")
        json.to_json(path_or_buf=filename, index=False, indent=4)

    return json


def main() -> None:
    json: DataFrame = getJSONResponse()
    print("Total documents found:", json.shape[0])


if __name__ == "__main__":
    main()
