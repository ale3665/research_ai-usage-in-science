from pathlib import Path
from typing import List

import click
import pandas
from pandas import DataFrame
from progress.bar import Bar
from pyfs import isFile, resolvePath
from requests import Response, get

from aius.downloadPapers import Journal_ABC
from aius.downloadPapers.nature import Nature
from aius.downloadPapers.plos import PLOS
from aius.downloadPapers.science import Science


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a journal's search result pickled object",
)
def main(inputPath: Path) -> None:
    absInputPath: Path = resolvePath(path=inputPath)

    assert isFile(path=absInputPath)

    data: dict[str, List[str | int | bytes]] = {
        "journal": [],
        "url": [],
        "status_code": [],
        "html": [],
    }

    df: DataFrame = pandas.read_pickle(filepath_or_buffer=absInputPath)
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
    outputDF.to_pickle(path="output.pickle")


if __name__ == "__main__":
    main()
