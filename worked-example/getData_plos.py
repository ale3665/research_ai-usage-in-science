from os.path import isfile
from pathlib import Path
from typing import List

import click
import pandas
from common import ifFileExistsExit, saveDFToJSON
from pandas import DataFrame
from progress.bar import Bar
from requests import Response, get


def getJSONResponse(fp: Path) -> DataFrame:
    json: DataFrame
    if isfile(path=fp):
        json = pandas.read_json(path_or_buf=fp)

    else:
        dfs: List[DataFrame] = []

        with Bar("Getting JSON responses...", max=1) as bar:
            page: int
            for page in range(1, 2):
                # Query: "Deep Learning"
                # Year: 2016
                # Page: 1
                # Max page: 1
                url: str = (
                    f"https://journals.plos.org/plosone/dynamicSearch?filterArticleTypes=Research%20Article&filterStartDate=2016-01-01&filterEndDate=2016-12-31&resultsPerPage=60&unformattedQuery=%22Deep%20Learning%22&q=%22Deep%20Learning%22&page={page}"  # noqa: E501
                )

                resp: Response = get(url=url, timeout=60)
                json = resp.json()

                dfs.append(DataFrame(data=json["searchResults"]["docs"]))

                bar.next()

        json = pandas.concat(objs=dfs, ignore_index=True)
        json["id"] = json["id"].apply(lambda x: f"https://doi.org/{x}")
        saveDFToJSON(df=json, filename=fp)

    return json


@click.command()
@click.option(
    "-o",
    "--output",
    "outputPath",
    required=True,
    help="Path to save PLOS search results",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
        path_type=Path,
    ),
)
def main(outputPath: Path) -> None:
    ifFileExistsExit(fps=[outputPath])

    json: DataFrame = getJSONResponse()
    print("Total documents found:", json.shape[0])


if __name__ == "__main__":
    main()
