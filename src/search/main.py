from itertools import product
from pathlib import Path
from string import Template
from typing import List

import click
import pandas
from pandas import DataFrame
from pyfs import isDirectory, isFile, resolvePath

from src.classes.journalGeneric import Journal_ABC
from src.classes.plos import PLOS
from src.utils.search import RELEVANT_YEARS, SEARCH_QUERIES

MEGA_JOURNAL_HELP_TEMPLATE: Template = Template(
    template="Search for documents in ${journal} mega journal",
)


def runCollector(journal: Journal_ABC) -> DataFrame:
    """
    Collects data from a specified journal using predefined search queries and years.

    This function orchestrates the process of gathering articles from a specific
    journal. It iterates over combinations of predefined search queries and years,
    conducts searches, and aggregates the results into a single DataFrame. It also
    removes duplicate entries based on URLs to ensure that each article is unique.

    :param journal: The journal from which data is to be collected. This object
                    must adhere to the Journal_ABC interface, which includes a
                    method for conducting searches given a query and a year.
    :type journal: Journal_ABC
    :return: A DataFrame containing aggregated results of all searches performed,
             with duplicates removed. The DataFrame includes article metadata such
             as titles, authors, publication dates, and URLs.
    :rtype: DataFrame
    """  # noqa: E501
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
    type=click.Choice(choices=["plos"]),
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
    """
    Main function to execute the data collection process for specified journal types.

    This function orchestrates the data collection from a specific journal by:
    1. Resolving the output file path.
    2. Ensuring the output file does not preexist to prevent overwriting.
    3. Matching the input journal type to its corresponding class.
    4. Running the data collector to gather and consolidate data.
    5. Saving the collected data to a Parquet file at the specified output path.

    :param outputPath: The path where the collected data will be stored as a Parquet file.
                       The function will exit if a file or directory already exists at this path.
    :type outputPath: Path
    :param journal: The identifier for the journal type to collect data from. Supported types
                    include 'nature' and 'plos'.
    :type journal: str
    """  # noqa: E501
    absOutputPath: Path = resolvePath(path=outputPath)

    if isFile(path=absOutputPath):
        print(f"{absOutputPath} already exists.")
        exit(1)

    if isDirectory(path=absOutputPath):
        print(f"{absOutputPath} is a directory")
        exit(1)

    journalClass: Journal_ABC
    match journal:
        case "plos":
            journalClass = PLOS()
        case _:
            exit(1)

    df: DataFrame = runCollector(journal=journalClass)

    df.to_parquet(path=absOutputPath, engine="pyarrow")


if __name__ == "__main__":
    main()
