import warnings
from pathlib import Path
from typing import List

import click
import pandas
from feedparser import FeedParserDict
from pandas import DataFrame
from progress.bar import Bar
from pyfs import resolvePath
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import IntegrityError

from lrac.captureRSSFeeds.db.schema import createSchema
from lrac.captureRSSFeeds.science import RSS_FEEDS, parser

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
def main(outputDB: Path) -> None:
    data: List[DataFrame] = []

    dbEngine: Engine = create_engine(url=f"sqlite:///{resolvePath(path=outputDB)}")
    dbTableName: str = createSchema(engine=dbEngine)

    with Bar(
        "Getting latest RSS feeds from known journals...",
        max=len(RSS_FEEDS),
    ) as bar:
        journal: str
        for journal in RSS_FEEDS.keys():
            feed: FeedParserDict = parser.getRSSFeed(feedURL=RSS_FEEDS[journal])
            data.append(parser.parseFeed(feed=feed))
            bar.next()

    df: DataFrame = pandas.concat(objs=data, ignore_index=True)
    writeToDB(df=df, dbTableName=dbTableName, dbEngine=dbEngine)


if __name__ == "__main__":
    main()
