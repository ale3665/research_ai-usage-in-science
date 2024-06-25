from pathlib import Path

import click
import pandas
from pandas import DataFrame
from pyfs import isDirectory, isFile, resolvePath

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
    help="Path to a journal's paper parquet file",
)
@click.option(
    "-o",
    "--output",
    "outputDir",
    type=Path,
    required=True,
    help="Directory to save Zettels to",
)
def main(inputPath: Path, outputDir: Path) -> None:
    absInputPath: Path = resolvePath(path=inputPath)
    absOutputDirPath: Path = resolvePath(path=outputDir)

    assert isFile(path=absInputPath)
    assert isDirectory(path=absOutputDirPath)

    df: DataFrame = pandas.read_parquet(path=absInputPath, engine="pyarrow")
    journalName: str = df["journal"][0]

    journal: Journal_ABC
    match journalName:
        case "Nature":
            journal = Nature()
        case "PLOS":
            journal = PLOS()
        # case "Science":
        #     journal = Science()
        case _:
            print("Unsupported journal")
            exit(1)


if __name__ == "__main__":
    main()
