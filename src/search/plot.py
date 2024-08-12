from pathlib import Path

import click
import matplotlib.pyplot as plt
import pandas
import seaborn as sns
from pandas import DataFrame
from pandas.core.groupby.generic import DataFrameGroupBy

from src.utils import ifFileExistsExit


def plotBarValues(data: dict) -> None:
    for i, (_, value) in enumerate(zip(data.keys(), data.values())):
        plt.text(
            i,
            value + 0.25,
            str(int(value)),
            ha="center",
            color="black",
        )


def plotResultsPerYear(df: DataFrame, fp: Path) -> None:
    data: dict[int, int] = {}

    dfgb: DataFrameGroupBy = df.groupby(by="year")

    year: int
    datum: DataFrame
    for year, datum in dfgb:
        data[year] = datum.shape[0]

    sns.barplot(data=data)
    plt.title(
        label=f"{df['journal'][0]} Journal Search Result Pages Per Year",
    )
    plt.xlabel(xlabel="Year")
    plt.ylabel(ylabel="Search Result Pages")

    plotBarValues(data=data)

    plt.tight_layout()
    plt.savefig(fp)
    plt.clf()


def plotQueriesPerYear(df: DataFrame, fp: Path) -> None:
    data: dict[int, int] = {}

    dfgb: DataFrameGroupBy = df.groupby(by="query")

    year: int
    datum: DataFrame
    for year, datum in dfgb:
        data[year] = datum.shape[0]

    sns.barplot(data=data)
    plt.title(
        label=f"{df['journal'][0]} Journal Search Result Pages Per Year",
    )
    plt.xlabel(xlabel="Search Query")
    plt.xticks(rotation=-45, ha="left")
    plt.ylabel(ylabel="Search Result Pages")

    plotBarValues(data=data)

    plt.tight_layout()
    plt.savefig(fp)
    plt.clf()


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to search results parquet file to plot data from",
)
@click.option(
    "--fig-1",
    "fig1Path",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to store figure 1",
)
@click.option(
    "--fig-2",
    "fig2Path",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to store figure 2",
)
def main(inputPath: Path, fig1Path: Path, fig2Path: Path) -> None:
    ifFileExistsExit(fps=[fig1Path, fig2Path])

    print(f'Reading "{inputPath}... ')
    df: DataFrame = pandas.read_parquet(path=inputPath, engine="pyarrow")

    print("Plotting search results per year...")
    plotResultsPerYear(df=df, fp=fig1Path)

    print("Plotting search results per query...")
    plotQueriesPerYear(df=df, fp=fig2Path)


if __name__ == "__main__":
    main()
