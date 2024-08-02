from pathlib import Path
from typing import List

import click
import pandas
from pandas import DataFrame
from pyfs import resolvePath


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to downloaded academic papers",
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
    print(absOutputPath)

    data: dict[str, List[str]] = {
        "url": [],
        "titles": [],
        "abstracts": [],
        "content": [],
        "tags": [],
    }

    df: DataFrame = pandas.read_parquet(path=absInputPath)

    print(df)
    print(data)


if __name__ == "__main__":
    main()
