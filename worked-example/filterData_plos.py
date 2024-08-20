from pathlib import Path
from typing import List

import click
import pandas
from common import ifFileExistsExit, saveDFToJSON
from pandas import DataFrame
from progress.bar import Bar
from requests import Response, get

FIELD_FILTER: set[str] = {
    "Agricultural and Biological Sciences",
    "Environmental Science",
    "Biochemistry Genetics and Molecular Biology",
    "Immunology and Microbiology",
    "Neuroscience",
    "Earth and Planetary Sciences",
    "Physics and Astronomy",
    "Chemistry",
    "Materials Science",
}


def filterWithOpenAlex(df: DataFrame) -> DataFrame:
    data: dict[str, List[str | bool | List[str]]] = {
        "doi": [],
        "field": [],
        "ns": [],
    }

    with Bar("Filtering data through OpenAlex...", max=df.shape[0]) as bar:
        doi: str
        for doi in df["id"]:
            url: str = f"https://api.openalex.org/works/{doi}"
            resp: Response = get(url=url, timeout=60)

            json: dict = resp.json()

            if json["cited_by_count"] == 0:
                bar.next()
                continue

            # field: dict = json["primary_topic"]["field"]["display_name"]

            fields: List[str] = [
                topic["field"]["display_name"] for topic in json["topics"]
            ]

            data["doi"].append(doi)
            data["field"].append(fields)
            data["ns"].append(
                (
                    True
                    if sum([x in FIELD_FILTER for x in fields]) > 1
                    else False
                ),
            )

            bar.next()

    return DataFrame(data=data)


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    required=True,
    help="Path to PLOS search results",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "--sample-output",
    "sampleOutput",
    required=True,
    help="Path to store sampled data",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "--filter-output",
    "filterOutput",
    required=True,
    help="Path to store filtered sample data",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "--sample-frac",
    "sampleFrac",
    required=False,
    default=0.5,
    help="Fraction of data to sample (float; 0 - 1.0)",
    type=float,
    show_default=True,
)
def main(
    inputPath: Path,
    sampleOutput: Path,
    filterOutput: Path,
    sampleFrac: float,
) -> None:
    df: DataFrame
    ifFileExistsExit(fps=[sampleOutput, filterOutput])

    json: DataFrame = pandas.read_json(path_or_buf=inputPath)
    sampledDF: DataFrame = json.sample(
        frac=sampleFrac,
        replace=False,
        random_state=42,
        ignore_index=True,
    )

    saveDFToJSON(df=sampledDF, filename=sampleOutput)

    df: DataFrame = filterWithOpenAlex(df=sampledDF)

    saveDFToJSON(df=df, filename=filterOutput)

    print(
        "Number of documents with valid tag:",
        df[df["ns"] == True].shape[0],  # noqa: E712
    )
    print(
        "Number of documents with invalid tag:",
        df[df["ns"] == False].shape[0],  # noqa: E712
    )


if __name__ == "__main__":
    main()
