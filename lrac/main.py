import inspect
import warnings
from abc import ABCMeta
from types import ModuleType
from typing import List

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

warnings.filterwarnings(action="ignore")


def findSubclasses(module: ModuleType, abc: ABCMeta) -> List[ABCMeta]:
    subclasses = []
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, abc) and obj != abc:
            subclasses.append(obj)
    return subclasses


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


def main() -> None:
    entries: List[DataFrame] = []
    parser: Parser = Parser()

    # TODO: Make this URL parametric
    dbEngine: Engine = create_engine(url="sqlite:///temp.db")
    dbTableName: str = createSchema(engine=dbEngine)

    journalClasses: List[ABCMeta] = findSubclasses(module=journals, abc=Journal)

    with Bar(
        "Getting latest RSS feeds from known journals...", max=len(journalClasses)
    ) as bar:
        jc: ABCMeta
        for jc in journalClasses:
            parser.getFeed(source=jc())
            entries.append(parser.parseFeed())
            bar.next()

    df: DataFrame = pandas.concat(objs=entries, ignore_index=True)
    writeToDB(df=df, dbTableName=dbTableName, dbEngine=dbEngine)


if __name__ == "__main__":
    main()
