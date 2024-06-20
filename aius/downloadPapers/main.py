from pathlib import Path
from typing import List

import click
import pandas
from pandas import DataFrame
from progress.bar import Bar
from pyfs import isFile, resolvePath

from aius.downloadPapers import Journal_ABC
from aius.downloadPapers.nature import Nature
from aius.downloadPapers.plos import PLOS


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

    df: DataFrame = pandas.read_pickle(filepath_or_buffer=absInputPath)
    journalName: str = df["journal"].value_counts().idxmax()
    resultCount: int = df.shape[0]

    # print(df["url"][0])
    # quit()

    journal: Journal_ABC
    match journalName:
        case "Nature":
            journal = Nature()
        case "PLOS":
            journal = PLOS()
        case "science":
            return "Science"
        case _:
            print("Unsupported journal")
            exit(1)

    paperURLs: List[str] = []
    with Bar("Identifying papers from HTML...", max=resultCount) as bar:
        html: str
        for html in df["html"]:
            paperURLs.extend(journal.getPaperURLs(html=html))
            bar.next()

    from pprint import pprint

    pprint(paperURLs)


if __name__ == "__main__":
    main()
