from itertools import product
from pathlib import Path
from string import Template
from typing import List

import click
import pandas
from pandas import DataFrame
from pyfs import resolvePath

from src.journals import Journal_ABC
from src.journals.nature import Nature
from src.journals.plos import PLOS
from src.utils.search import RELEVANT_YEARS, SEARCH_QUERIES

MEGA_JOURNAL_HELP_TEMPLATE: Template = Template(
    template="Search for documents in ${journal} mega journal",
)


def runCollector(journal: Journal_ABC) -> DataFrame:
    data: List[DataFrame] = []

    for pair in product(SEARCH_QUERIES, RELEVANT_YEARS):
        df: DataFrame = journal.conductSearch(query=pair[0], year=pair[1])
        data.append(df)

    df: DataFrame = pandas.concat(objs=data, ignore_index=True)
    df.drop_duplicates(
        subset=["url"],
        keep="first",
        inplace=True,
        ignore_index=True,
    )

    return df


@click.command()
@click.option(
    "-j",
    "--journal",
    "journal",
    required=True,
    type=click.Choice(choices=["nature", "plos"]),
    help="Search for documents in a supported mega-journal",
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    required=True,
    type=Path,
    help="Output parquet file to save Pandas DataFrame to",
)
def main(outputPath: Path, journal: str) -> None:
    absOutputPath: Path = resolvePath(path=outputPath)

    journalClass: Journal_ABC
    match journal:
        case "nature":
            journalClass = Nature()
        case "plos":
            journalClass = PLOS()
        case _:
            exit(1)

    df: DataFrame = runCollector(journal=journalClass)

    df.to_parquet(path=absOutputPath, engine="pyarrow")


if __name__ == "__main__":
    main()
