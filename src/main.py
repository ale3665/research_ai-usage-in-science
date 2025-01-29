import sys
from argparse import ArgumentParser, Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

from src.db import DB
from src.utils import ifFileExistsExit

COMMANDS: set[str] = {"init"}


def cliParser() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="aius",
        description="Identify AI usage in Natural Science research",
    )
    subparser: _SubParsersAction[ArgumentParser] = parser.add_subparsers()

    initParser: ArgumentParser = subparser.add_parser(
        name="init",
        help="Initialize AIUS",
        aliases="init",
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
    return parser.parse_args()


def initialize(fp: Path) -> None:
    ifFileExistsExit(fps=[fp])
    db: DB = DB(fp=fp)
    db.createTables()


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

    sys.exit(0)


if __name__ == "__main__":
    main()
