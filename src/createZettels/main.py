from pathlib import Path

import click
import pandas
from pandas import DataFrame
from pyfs import isFile, resolvePath


def main() -> None:
    inputPath: Path = Path("../../data/plos/parquet/papers.parquet")

    absInputPath: Path = resolvePath(path=inputPath)

    assert isFile(path=absInputPath)

    df: DataFrame = pandas.read_parquet(path=absInputPath, engine="pyarrow")


if __name__ == "__main__":
    main()
