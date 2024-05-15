from pathlib import Path
from string import Template
from typing import List

import click
from pyfs import resolvePath
from src.search.nature import Nature
from src.search.plos import PLOS
from src.search.science import Science

MEGA_JOURNAL_HELP_TEMPLATE: Template = Template(
    template="Search for documents in ${journal} mega journal",
)


# TODO: Check for a pre-made solution for this function
def checkForOneFlag(flags: List[bool]) -> bool:
    total: int = sum(flags)

    if total == 1:
        return True
    else:
        return False


@click.command()
@click.option(
    "-o",
    "--ouput",
    "output",
    required=True,
    type=Path,
    help="Path to save search results to",
)
@click.option(
    "--nature",
    required=False,
    is_flag=True,
    help=MEGA_JOURNAL_HELP_TEMPLATE.substitute(journal="Nature"),
)
@click.option(
    "--plos",
    required=False,
    is_flag=True,
    help=MEGA_JOURNAL_HELP_TEMPLATE.substitute(journal="PLOS"),
)
@click.option(
    "--science",
    required=False,
    is_flag=True,
    help=MEGA_JOURNAL_HELP_TEMPLATE.substitute(journal="Science"),
)
def main(
    output: Path,
    nature: bool = False,
    plos: bool = False,
    science: bool = False,
) -> None:
    if checkForOneFlag(flags=[nature, plos, science]) == False:
        print("Only one journal can be selected at a time. Please select one ")

    outputPath: Path = resolvePath(path=output)


if __name__ == "__main__":
    main()
