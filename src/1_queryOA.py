from json import loads
from pathlib import Path
from string import Template
from typing import List

import click
import pandas
from pandas import DataFrame, Series
from progress.bar import Bar
from requests import Response, get

from src.utils import ifFileExistsExit


def extractDOIs(df: DataFrame, journal: str) -> DataFrame:
    data: dict[str, List] = {
        "year": [],
        "query": [],
        "page": [],
        "journal": [],
        "doi": [],
    }

    row: Series
    for _, row in df.iterrows():
        if journal == "plos":
            json: dict = loads(s=row["html"])
            docs: List[dict] = json["searchResults"]["docs"]

            doc: dict
            for doc in docs:
                data["year"].append(row["year"])
                data["query"].append(row["query"])
                data["page"].append(row["page"])
                data["journal"].append(row["journal"])
                data["doi"].append(f"https://doi.org/{doc['id']}")

    return DataFrame(data=data)


def queryOA(email: str, df: DataFrame) -> DataFrame:
    data: dict[str, List] = {"status_code": [], "json": []}

    urlTemplate: Template = Template(
        template="https://api.openalex.org/works/${doi}?mailto=" + email
    )

    with Bar("Querying OpenAlex...", max=df.shape[0]) as bar:
        row: Series
        for _, row in df.iterrows():
            url: str = urlTemplate.substitute(doi=row["doi"])
            resp: Response = get(url=url, timeout=60)
            data["status_code"].append(resp.status_code)
            data["json"].append(resp.content)
            bar.next()

    df["status_code"] = data["status_code"]
    df["json"] = data["json"]

    return df


@click.command()
@click.option(
    "-e",
    "--email",
    "email",
    type=str,
    required=True,
    help="Email address to access OpenAlex polite pool",
)
@click.option(
    "-j",
    "--journal",
    "journal",
    type=click.Choice(choices=["plos"], case_sensitive=False),
    required=True,
    help="Journal of search results file",
)
@click.option(
    "-i",
    "--input",
    "inputFP",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to input file",
)
@click.option(
    "-o",
    "--output",
    "outputFP",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to input file",
)
def main(email: str, journal: str, inputFP: Path, outputFP: Path) -> None:
    ifFileExistsExit(fps=[outputFP])

    df: DataFrame = pandas.read_parquet(path=inputFP, engine="pyarrow")

    df: DataFrame = extractDOIs(df=df, journal=journal)
    df = queryOA(email=email, df=df)

    df.to_parquet(path=outputFP, engine="pyarrow")


if __name__ == "__main__":
    main()
