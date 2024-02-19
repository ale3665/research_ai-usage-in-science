import inspect
from abc import ABCMeta
from types import ModuleType
from typing import List

import pandas
from pandas import DataFrame
from progress.bar import Bar

from lrac.classes import journals
from lrac.classes.journals import Journal
from lrac.classes.parser import Parser


def findSubclasses(module: ModuleType, abc: ABCMeta) -> List[ABCMeta]:
    subclasses = []
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, Journal) and obj != abc:
            subclasses.append(obj)
    return subclasses


def main() -> None:
    entries: List[DataFrame] = []
    parser: Parser = Parser()

    journalClasses: List[ABCMeta] = findSubclasses(module=journals, abc=Journal)

    with Bar(
        "Getting latest RSS feeds from known journals...", max=len(journalClasses)
    ) as bar:
        jc: ABCMeta
        for jc in journalClasses:
            parser.getFeed(source=jc())
            entries.append(parser.parseFeed())
            parser.clear()
            bar.next()

    df: DataFrame = pandas.concat(objs=entries, ignore_index=True)
    df.to_csv(path_or_buf="temp.csv", index=False)


if __name__ == "__main__":
    main()
