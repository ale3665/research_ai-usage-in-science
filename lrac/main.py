import inspect
import warnings
from abc import ABCMeta
from pathlib import Path
from types import ModuleType
from typing import List

import click
import pandas
from pandas import DataFrame
from progress.bar import Bar
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import IntegrityError

from lrac.classes import journals
from lrac.classes.journals import Journal
from lrac.classes.parser import Parser
from lrac.db.schema import createSchema
from lrac.utils.metaprogramming import findSubclasses

warnings.filterwarnings(action="ignore")


def writeToDB(df: DataFrame, dbTableName: str, dbEngine: Engine) -> None:
    dfPerRow: List[DataFrame] = [DataFrame(data=row).T for _, row in df.iterrows()]

    with Bar("Writing data to database...", max=len(dfPerRow)) as bar:
        row: DataFrame
        for row in dfPerRow:
            try:
                row.to_sql(
                    name=dbTableName, con=dbEngine, index=False, if_exists="append"
                )
            except IntegrityError:
                pass

            bar.next()


@click.command()
@click.option(
    "outputDB",
    "-o",
    "--output",
    help="Path to SQLite3 database (.db) file to write content to",
    required=True,
    type=Path,
)
@click.option(
    "rssStore",
    "-r",
    "--rss",
    help="Path to directory to write RSS JSON files (.json) to",
    required=True,
    type=Path,
)
@click.option(
    "pdfStore",
    "-p",
    "--pdf",
    help="Path to directory to write PDF files (.pdf) to",
    required=True,
    type=Path,
)
def main(outputDB: Path, rssStore: Path, pdfStore: Path) -> None:
    entries: List[DataFrame] = []
    parser: Parser = Parser()

    dbEngine: Engine = create_engine(url=f"sqlite:///{outputDB}")
    dbTableName: str = createSchema(engine=dbEngine)

    journalClasses: List[ABCMeta] = findSubclasses(module=journals, abc=Journal)

    with Bar(
        "Getting latest RSS feeds from known journals...", max=len(journalClasses)
    ) as bar:
        jc: ABCMeta
        for jc in journalClasses:
            parser.getFeed(source=jc(), rssStore=rssStore)
            entries.append(parser.parseFeed(pdfStore=pdfStore))
            bar.next()

    df: DataFrame = pandas.concat(objs=entries, ignore_index=True)
    writeToDB(df=df, dbTableName=dbTableName, dbEngine=dbEngine)


if __name__ == "__main__":
    main()
