from json import loads
from pathlib import Path

import click
import pandas
from pandas import DataFrame, Series


def extractDOIs(df: DataFrame, journal: str) -> DataFrame:
    row: Series
    for _, row in df.iterrows():
        if journal == "plos":
            data: dict = loads(s=row["html"])
            print(data["searchResults"]["docs"])
            quit()


@click.command()
@click.option(
    "-j",
    "--journal",
    "journal",
    type=click.Choice(choices=["plos", "nature"], case_sensitive=False),
    required=True,
    help="Journal of search results file",
)
def main(journal: str) -> None:
    df: DataFrame = pandas.read_parquet(
        path=Path("../data/plos_search-results.parquet"), engine="pyarrow"
    )

    extractDOIs(df=df, journal=journal)


if __name__ == "__main__":
    main()
