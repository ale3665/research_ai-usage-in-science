from collections import defaultdict
from json import loads
from pathlib import Path
from pprint import pprint

import click
import pandas
from pandas import DataFrame, Series
from pandas.core.groupby import DataFrameGroupBy


def countSearchResultsPerYear(df: DataFrame, journal: str) -> Series:
    data: dict[int, int] = defaultdict(int)
    dfgb: DataFrameGroupBy = df.groupby(by="year")

    year: int
    _df: DataFrame
    row: DataFrame
    for year, _df in dfgb:
        uniqueSearchQueriesDF: DataFrame = _df.drop_duplicates(
            subset="query",
            keep="first",
            ignore_index=True,
        )

        for _, row in uniqueSearchQueriesDF.iterrows():
            if journal == "plos":
                data[year] += int(
                    loads(s=row["html"])["searchResults"]["numFound"]
                )

    return Series(data=data)


def countSearchResultsPerQuery(df: DataFrame, journal: str) -> Series:
    data: dict[str, int] = defaultdict(int)
    dfgb: DataFrameGroupBy = df.groupby(by="query")

    query: str
    _df: DataFrame
    row: DataFrame
    for query, _df in dfgb:
        uniqueYearsDF: DataFrame = _df.drop_duplicates(
            subset="year",
            keep="first",
            ignore_index=True,
        )

        for _, row in uniqueYearsDF.iterrows():
            if journal == "plos":
                data[query] += int(
                    loads(s=row["html"])["searchResults"]["numFound"]
                )

    return Series(data=data)


def countSearchResultsPerYearPerQuery(df: DataFrame, journal: str) -> Series:
    data: dict[int, dict[str, int]] = {}
    dfgb: DataFrameGroupBy = df.groupby(by="year")

    year: int
    _df: DataFrame
    row: DataFrame
    for year, _df in dfgb:
        data[year] = {}
        uniqueSearchQueriesDF: DataFrame = _df.drop_duplicates(
            subset="query",
            keep="first",
            ignore_index=True,
        )

        for _, row in uniqueSearchQueriesDF.iterrows():
            if journal == "plos":
                data[year][row["query"]] = int(
                    loads(s=row["html"])["searchResults"]["numFound"]
                )

    return Series(data=data)


@click.command()
@click.option(
    "-j",
    "--journal",
    "journal",
    required=True,
    type=click.Choice(
        choices=["plos", "nature"],
        case_sensitive=False,
    ),
    help="Search results journal name",
)
@click.option(
    "-i",
    "--input",
    "inputFP",
    required=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    help="Document containing search results",
)
def main(journal: str, inputFP: Path) -> None:
    df: DataFrame = pandas.read_parquet(
        path=inputFP,
        engine="pyarrow",
    )

    print(f"{journal} Data\n===")
    results: Series = countSearchResultsPerYear(df=df, journal=journal)
    total: int = results.sum()
    print(f"Results Per Year\n{results}\nTotal: {total}\n===")

    results: Series = countSearchResultsPerQuery(df=df, journal=journal)
    total: int = results.sum()
    print(f"Results Per Query\n{results}\nTotal: {total}\n===")

    results: Series = countSearchResultsPerYearPerQuery(df=df, journal=journal)
    print("Results Per Year Per Query")
    pprint(results.to_dict(), indent=4)


if __name__ == "__main__":
    main()
