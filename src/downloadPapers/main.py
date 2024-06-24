from pathlib import Path
from typing import List

import click
import pandas
from pandas import DataFrame
from progress.bar import Bar
from pyfs import isFile, resolvePath
from requests import Response, get

from src.downloadPapers import Journal_ABC
from src.downloadPapers.nature import Nature
from src.downloadPapers.plos import PLOS
from src.downloadPapers.science import Science


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a journal's search result parquet file",
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    type=Path,
    required=True,
    help="Path to save journal paper parquet file",
)
def main(inputPath: Path, outputPath: Path) -> None:
    absInputPath: Path = resolvePath(path=inputPath)
    absOutputPath: Path = resolvePath(path=outputPath)

    assert isFile(path=absInputPath)

    data: dict[str, List[str | int | bytes]] = {
        "journal": [],
        "url": [],
        "status_code": [],
        "html": [],
    }

    df: DataFrame = pandas.read_parquet(path=absInputPath, engine="pyarrow")
    journalName: str = df["journal"].value_counts().idxmax()
    resultCount: int = df.shape[0]

    journal: Journal_ABC
    match journalName:
        case "Nature":
            journal = Nature()
        case "PLOS":
            journal = PLOS()
        case "Science":
            journal = Science()
        case _:
            print("Unsupported journal")
            exit(1)

    paperURLs: List[str] = []
    with Bar("Identifying papers from HTML...", max=resultCount) as bar:
        html: str
        for html in df["html"]:
            paperURLs.extend(journal.getPaperURLs(html=html))
            bar.next()

    with Bar("Downloading papers...", max=len(paperURLs)) as bar:
        url: str
        for url in paperURLs:
            data["journal"].append(journal)
            data["url"].append(url)

            resp: Response = get(url=url)

            data["status_code"].append(resp.status_code)
            data["html"].append(resp.content)

            bar.next()

    outputDF: DataFrame = DataFrame(data=data)
    outputDF.to_parquet(path=absOutputPath, engine="pyarrow")


if __name__ == "__main__":
    main()
