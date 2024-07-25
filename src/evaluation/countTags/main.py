from pathlib import Path
from sqlite3 import Connection, connect

import click
import pandas
from pandas import DataFrame, Series
from pyfs import resolvePath


def readDB(dbPath: Path) -> DataFrame:
    sql: str = "SELECT tags FROM zettels"
    conn: Connection = connect(database=dbPath)
    df: DataFrame = pandas.read_sql_query(sql=sql, con=conn)
    df["tags"] = df["tags"].apply(lambda x: x.split("✖"))
    conn.close()
    return df


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a Zettelgeist database",
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    type=Path,
    required=True,
    help="Path to store data in CSV format",
)
def main(inputPath: Path, outputPath: Path) -> None:
    absInputPath: Path = resolvePath(path=inputPath)
    absOutputPath: Path = resolvePath(path=outputPath)

    df: DataFrame = readDB(dbPath=absInputPath)

    explodedDF: DataFrame = df.explode(column="tags", ignore_index=True)
    explodedDF["tags"] = explodedDF["tags"].str.strip("️")

    tagCounts: Series = explodedDF.value_counts(subset="tags")

    tagCounts.to_csv(path_or_buf=absOutputPath)


if __name__ == "__main__":
    main()
