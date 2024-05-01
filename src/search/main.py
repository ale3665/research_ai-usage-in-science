from pathlib import Path
from string import Template

import click

MEGA_JOURNAL_HELP_TEMPLATE: Template = Template(
    template="Search for documents in ${journal} mega journal",
)


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
    print(nature)
    print(plos)
    print(science)


if __name__ == "__main__":
    main()
