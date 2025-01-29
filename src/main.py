import sys
from argparse import ArgumentParser, Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

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


def initialize(fp: Path) -> None:
    ifFileExistsExit(fps=[fp])
    DB(fp=fp).createTables()


def search(fp: Path, journal: str) -> None:
    initialize(fp=fp)
    print(fp, journal)


def main() -> None:
    args: dict[str, Any] = cliParser().__dict__

    argSet: set[str] = set([cmd.split(".")[0] for cmd in args.keys()])

    try:
        arg: str = list(argSet.intersection(COMMANDS))[0]
    except IndexError:
        sys.exit(0)

    match arg:
        case "init":
            initialize(fp=args["init.db"])
        case "search":
            search(fp=args["search.db"], journal=args["search.journal"])

    sys.exit(0)


if __name__ == "__main__":
    main()
