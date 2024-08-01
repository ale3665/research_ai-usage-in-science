from pathlib import Path
from time import sleep
from typing import List

import click
import pandas
from pandas import DataFrame, Series
from progress.bar import Bar
from pyfs import resolvePath
from requests import Response

from src.classes.journalGeneric import Journal_ABC
from src.classes.openalex import OpenAlex
from src.classes.plos import PLOS


def getPaperDOIs(source: Journal_ABC, df: DataFrame) -> DataFrame:
    data: dict[str, List[str]] = {"urls": []}

    searchResultsHTML: Series = df["html"]

    with Bar(
        "Extracting paper URLs from search results...",
        max=searchResultsHTML.size,
    ) as bar:
        result: str
        for result in searchResultsHTML:
            urls: List[str] = source.extractPaperURLsFromSearchResult(
                respContent=result
            )
            data["urls"].extend(urls)
            bar.next()

        urlsDF: DataFrame = DataFrame(data=data)

        urlsDF["urls"] = urlsDF["urls"].apply(
            lambda x: f"https://doi.org/{source.extractDOIFromPaper(url=x)}"
        )

    return urlsDF


def getOpenAlexResults(df: DataFrame, email: str | None) -> DataFrame:
    oa: OpenAlex = OpenAlex(email=email)

    data: dict[str, List[str | int]] = {
        "doi": [],
        "api_call": [],
        "status_code": [],
        "json": [],
    }

    with Bar(
        "Getting OpenAlex metadata for each paper...",
        max=df.shape[0],
    ) as bar:
        url: str
        for url in df["urls"]:
            resp: Response | None = oa.searchByDOI(doiURL=url)

            resp = None

            if resp is None:
                data["doi"].append(url)
                data["api_call"].append("")
                data["status_code"].append(404)
                data["json"].append("")
                bar.next()
                continue

            # TODO: Fix this code
            if resp.status_code == 429:
                sleep(11)
                resp: Response = oa.searchByDOI(doiURL=url)
                if resp.status_code == 429:
                    print("Possible rate limit reached. Exiting")
                    exit(2)

            data["doi"].append(url)
            data["api_call"].append(resp.url)
            data["status_code"].append(resp.status_code)
            data["json"].append(
                resp.content.decode(
                    errors="ignore",
                )
            )

            bar.next()

    return DataFrame(data=data)


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a parquet file containing journal search results",
)
@click.option(
    "-e",
    "--email",
    "email",
    type=str,
    required=False,
    help="A valid email which will allow for access to the OpenAlex API Polite Pool",  # noqa: E501
    default=None,
)
def main(inputPath: Path, email: str | None = None) -> None:
    absInputPath: Path = resolvePath(path=inputPath)

    df: DataFrame = pandas.read_parquet(path=absInputPath, engine="pyarrow")
    journal: str = df["journal"][0]

    source: Journal_ABC
    match journal:
        case "PLOS":
            source = PLOS()
        case _:
            exit(1)

    doisDF: DataFrame = getPaperDOIs(source=source, df=df)

    oaDF: DataFrame = getOpenAlexResults(
        df=doisDF,
        email=email,
    )

    # TODO: Change this to be a command line parameter
    oaDF.to_parquet(path="oa_plos.parquet", engine="pyarrow")


if __name__ == "__main__":
    main()
