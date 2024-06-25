from pathlib import Path

import click
import pandas
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
from progress.bar import Bar
from pyfs import isDirectory, isFile, resolvePath


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    required=True,
    type=Path,
    help="Path to parquet file to create HTML documents from",
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    required=True,
    type=Path,
    help="Path to a directory to save HTML documents to",
)
def main(inputPath: Path, outputPath: Path) -> None:
    absInputPath: Path = resolvePath(path=inputPath)
    absOutputPath: Path = resolvePath(path=outputPath)

    assert isFile(path=absInputPath)
    assert isDirectory(path=absOutputPath)

    df: DataFrame = pandas.read_parquet(path=absInputPath, engine="pyarrow")

    with Bar("Creating HTML files...", max=df.shape[0]) as bar:
        row: Series
        for _, row in df.iterrows():
            filepath: Path = Path(
                absOutputPath,
                f'{row["year"]}_{row["query"]}_{row["page"]}_{row["status_code"]}.html',
            )

            soup: BeautifulSoup = BeautifulSoup(
                markup=row["html"],
                features="lxml",
            )

            with open(file=filepath, mode="w") as htmlFile:
                htmlFile.write(soup.prettify())
                htmlFile.close()

            bar.next()


if __name__ == "__main__":
    main()
