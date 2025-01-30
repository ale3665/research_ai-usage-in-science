import sys
from argparse import ArgumentParser, Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

from pandas import DataFrame

from src import searchFunc
from src.db import DB
from src.utils import ifFileExistsExit

COMMANDS: set[str] = {"init", "search"}


def cliParser() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="aius",
        description="Identify AI usage in Natural Science research",
    )
    subparser: _SubParsersAction[ArgumentParser] = parser.add_subparsers()

    initParser: ArgumentParser = subparser.add_parser(
        name="init",
        help="Initialize AIUS (Step 0)",
    )
    initParser.add_argument(
        "-d",
        "--db",
        nargs=1,
        default=Path("aius.sqlite3"),
        type=Path,
        help="Path to create AIUS SQLite3 database",
        dest="init.db",
    )

    searchParser: ArgumentParser = subparser.add_parser(
        name="search",
        help="Search Journals (Step 1)",
    )
    searchParser.add_argument(
        "-d",
        "--db",
        nargs=1,
        default=Path("aius.sqlite3"),
        type=Path,
        help="Path to AIUS SQLite3 database",
        dest="search.db",
    )
    searchParser.add_argument(
        "-j",
        "--journal",
        nargs=1,
        default="plos",
        type=str,
        choices=["nature", "plos", "science"],
        help="Journal to search through",
        dest="search.journal",
    )

    return parser.parse_args()


def initialize(fp: Path) -> DB:
    ifFileExistsExit(fps=[fp])
    db: DB = DB(fp=fp)
    db.createTables()
    db.writeConstants()
    return db


def search(fp: Path, journal: str) -> None:
    df: DataFrame | None = None

    db: DB = DB(fp=fp)

    match journal:
        case "nature":
            df = searchFunc.nature()
        case "plos":
            df = searchFunc.plos()
        case "science":
            searchFunc.science()
            return None
        case _:
            return None

    df.to_sql(
        name="search_responses",
        con=db.engine,
        if_exists="append",
        index=False,
    )


def main() -> None:
    args: dict[str, Any] = cliParser().__dict__

    argSet: set[str] = set([cmd.split(".")[0] for cmd in args.keys()])

    try:
        arg: str = list(argSet.intersection(COMMANDS))[0]
    except IndexError:
        sys.exit(0)

    match arg:
        case "init":
            initialize(fp=args["init.db"][0])
        case "search":
            search(fp=args["search.db"][0], journal=args["search.journal"][0])

    sys.exit(0)


if __name__ == "__main__":
    main()
