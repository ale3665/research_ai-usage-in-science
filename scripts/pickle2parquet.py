from pathlib import Path

import click
import pandas
from pandas import DataFrame
from pyfs import isFile, resolvePath


def _exitIfFileDoesNotExist(path: Path) -> None:
    if isFile(path=path) == False:
        print(f"{path} is not a file")
        exit(1)


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a pickled Pandas DataFrame object",
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    type=Path,
    required=True,
    help="Path to save the Pandas DataFrame to a parquet file",
)
def main(inputPath: Path, outputPath: Path) -> None:
    absInputPath: Path = resolvePath(path=inputPath)
    absOutputPath: Path = resolvePath(path=outputPath)

    _exitIfFileDoesNotExist(path=absInputPath)
    _exitIfFileDoesNotExist(path=absOutputPath)

    print(f"Reading {absInputPath} ...")
    df: DataFrame = pandas.read_pickle(
        filepath_or_buffer=absInputPath,
    )  # nosec

    print(f"Writing {absOutputPath} ...")
    df.to_parquet(path=absOutputPath, engine="pyarrow")


if __name__ == "__main__":
    main()
