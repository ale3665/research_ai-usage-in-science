from json import loads
from pathlib import Path
from typing import List

import click
import pandas
from pandas import DataFrame
from pyfs import resolvePath
from toi import chat


@click.command()
@click.option(
    "systemPrompt",
    "-s",
    "--system-prompt",
    help="The system prompt to pass to the GPT model",
    required=False,
    default="Only return the top-10 scientific disciplines ordered from most probable to least probable for each title-abstract pair in JSON format",
    type=str,
)
@click.option(
    "apiKey",
    "-k",
    "--api-key",
    help="Your OpenAI GPT API key",
    required=True,
    type=str,
)
@click.option(
    "csvFile",
    "-i",
    "--csv-file-input",
    help="Path to a csv file to read from as input",
    required=True,
    type=Path,
)
def main(
    systemPrompt: str,
    apiKey: str,
    csvFile: Path,
) -> None:
    gptModel: str = "gpt-4-turbo-preview"

    csvFilePath: Path = resolvePath(path=csvFile)

    df: DataFrame = pandas.read_csv(filepath_or_buffer=csvFilePath).iloc[0:1]

    row: tuple[str, str, str]
    for row in df.itertuples(index=False):
        title: str = row[1]
        abstract: str = row[2]

        userPrompt: str = f"{title} : {abstract}"

        response: dict = chat(
            text=userPrompt,
            systemPrompt=systemPrompt,
            apiKey=apiKey,
            model=gptModel,
        )

        from pprint import pprint as print

        print(response)


if __name__ == "__main__":
    main()
