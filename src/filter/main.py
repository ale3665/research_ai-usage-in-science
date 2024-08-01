from pathlib import Path
from typing import List

import click
import pandas
from pandas import DataFrame, Series
from progress.bar import Bar
from pyfs import resolvePath

from src.classes.journalGeneric import Journal_ABC
from src.classes.plos import PLOS


def getPaperDOIs(source: Journal_ABC, df: DataFrame) -> DataFrame:
    data: dict[str, List[str]] = {"urls": []}

    searchResultsHTML: Series = df["html"]

    with Bar(
        "Extracting paper URLs from search results", max=searchResultsHTML.size
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


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a parquet file containing journal search results",
)
def main(inputPath: Path) -> None:
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

    print(doisDF)


if __name__ == "__main__":
    main()
