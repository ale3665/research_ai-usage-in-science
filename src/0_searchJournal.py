import sys
from itertools import product
from pathlib import Path
from typing import List

import click
import pandas
from pandas import DataFrame

from src.journals._generic import Journal_ABC
from src.journals.nature import Nature
from src.journals.plos import PLOS
from src.journals.science import Science
from src.utils import ifFileExistsExit

RELEVANT_YEARS: List[int] = list(range(2014, 2025))  # [2014, ..., 2025)

SEARCH_QUERIES: List[str] = [
    r'"Deep Learning"',
    r'"Deep Neural Network"',
    r'"Hugging Face"',
    r'"HuggingFace"',
    r'"Model Checkpoint"',
    r'"Model Weights"',
    r'"Pre-Trained Model"',
]


def runCollector(journal: Journal_ABC) -> DataFrame:
    data: List[DataFrame] = []

    for pair in product(SEARCH_QUERIES, RELEVANT_YEARS):
        df: DataFrame = journal.searchJournal(query=pair[0], year=pair[1])
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
    required=False,
    type=click.Choice(
        choices=["plos", "science", "nature"], case_sensitive=False
    ),
    help="Journal to search for documents in",
    default="plos",
    show_default=True,
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    required=True,
    help="Output parquet file to save Pandas DataFrame to",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
def main(outputPath: Path, journal: str) -> None:
    """
    Searches through a given journal and outputs a Pandas DataFrame stored as an Apache Parquet file with the search results.

    These search results are the raw outputs of the search meant to be post-processed for usage in other scripts.

    While the data outputted from this script can be leveraged independently, it is better to use this data in the following pipeline:

    **aius-search-journal** -> aius-filter-documents -> aius-sample-documents -> aius-download-documents
    """  # noqa: E501
    ifFileExistsExit(fps=[outputPath])

    journalClass: Journal_ABC | Science
    match journal:
        case "nature":
            journalClass = Nature()
        case "plos":
            journalClass = PLOS()
        case "science":
            journalClass = Science()
            print(
                """Due to section 6 subsection b of the AAAS Science terms of service (availible here: https://www.science.org/content/page/terms-service), we are unable to provide an automatic tool to extract or analyze the contents of the AAAS Science website (https://www.science.org).

Therefore, we will not be providing a tool, the information to produce such as tool, or the raw, untransformed content of the AAAS Science website in any form.

However, for manual analysis, the following URLs we do provide all of the necessary URLs to reproduce our work are now stored in `./science_urls.json`.
            """  # noqa: E501
            )

            journalClass.generateURLs(
                years=RELEVANT_YEARS,
                queries=SEARCH_QUERIES,
            ).to_json(
                path_or_buf="science_urls.json",
                indent=4,
            )

            sys.exit(0)

        case _:
            sys.exit(1)

    df: DataFrame = runCollector(journal=journalClass)

    df.to_parquet(path=outputPath, engine="pyarrow")


if __name__ == "__main__":
    main()
