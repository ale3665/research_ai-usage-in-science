from itertools import product
from pathlib import Path
from string import Template
from typing import List

import click
import pandas
from pandas import DataFrame
from pyfs import resolvePath

from aius.search import RELEVANT_YEARS, SEARCH_QUERIES, Journal_ABC
from aius.search.nature import Nature
from aius.search.plos import PLOS
from aius.search.science import Science

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
    "-o",
    "--output",
    "output",
    required=True,
    type=Path,
    help="Output pickle file to save Pandas DataFrame to",
)
@click.option(
    "--nature",
    required=False,
    is_flag=True,
    help=MEGA_JOURNAL_HELP_TEMPLATE.substitute(journal="Nature"),
)
@click.option(
    "--plos",
    required=False,
    is_flag=True,
    help=MEGA_JOURNAL_HELP_TEMPLATE.substitute(journal="PLOS"),
)
@click.option(
    "--science",
    required=False,
    is_flag=True,
    help=MEGA_JOURNAL_HELP_TEMPLATE.substitute(journal="Science"),
)
def main(
    output: Path,
    nature: bool = False,
    plos: bool = False,
    science: bool = False,
) -> None:
    flags: List[bool] = [nature, plos, science]
    flagCount: int = sum(flags)

    if flagCount > 1:
        raise click.UsageError("Only one journal can be used at a time.")
    elif flagCount < 1:
        raise click.UsageError("At least one journal must be selected")
    else:
        pass

    outputPath: Path = resolvePath(path=output)

    journal: Journal_ABC
    if nature:
        journal = Nature()
    if plos:
        journal = PLOS()
    if science:
        journal = Science()

    df: DataFrame = runCollector(journal=journal)

    df.to_pickle(path=outputPath)


if __name__ == "__main__":
    main()
