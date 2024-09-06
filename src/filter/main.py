from json import loads
from pathlib import Path
from time import sleep
from typing import List, Tuple

import click
import pandas
from pandas import DataFrame, Series
from progress.bar import Bar
from requests import Response

from src.classes.journalGeneric import Journal_ABC
from src.classes.openalex import OpenAlex
from src.classes.plos import PLOS
from src.utils import extractDOIsFromHTML, ifFileExistsExit

# TODO: Add filter lists for subfields and topics
FIELD_FILTER: set[str] = {
    "Agricultural and Biological Sciences",
    "Environmental Science",
    "Biochemistry Genetics and Molecular Biology",
    "Immunology and Microbiology",
    "Neuroscience",
    "Earth and Planetary Sciences",
    "Physics and Astronomy",
    "Chemistry",
}


def getOpenAlexResults(df: DataFrame, email: str | None) -> DataFrame:
    oa: OpenAlex = OpenAlex(email=email)

    data: dict[str, List[str | int]] = {
        "doi": [],
        "api_call": [],
        "status_code": [],
        "json": [],
    }

    with Bar(
        "Getting OpenAlex metadata for each paper...",
        max=df.shape[0],
    ) as bar:
        url: str
        for url in df["urls"]:
            resp: Response | None = oa.searchByDOI(doiURL=url)

            if resp is None:
                data["doi"].append(url)
                data["api_call"].append("")
                data["status_code"].append(404)
                data["json"].append("")
                bar.next()
                continue

            # TODO: Fix this code
            if resp.status_code == 429:
                sleep(11)
                resp: Response = oa.searchByDOI(doiURL=url)
                if resp.status_code == 429:
                    print("Possible rate limit reached. Exiting")
                    exit(2)

            data["doi"].append(url)
            data["api_call"].append(resp.url)
            data["status_code"].append(resp.status_code)
            data["json"].append(
                resp.content.decode(
                    errors="ignore",
                )
            )

            bar.next()

    return DataFrame(data=data)


def filterOAResults(
    oaDF: DataFrame,
    filterList: List[str],
    column: str,
    filterIntersection: int = 2,
    citedByMinimum: int = 1,
) -> DataFrame:
    dfs: List[DataFrame] = []

    df: DataFrame = oaDF[oaDF["status_code"] == 200].reset_index(drop=True)

    with Bar("Filtering academic papers...", max=df.shape[0]) as bar:
        row: Series
        for _, row in df.iterrows():
            oa: OpenAlex = OpenAlex()

            jsonStr: str = row["json"]
            json: dict = loads(s=jsonStr)

            ptDF: DataFrame | None = oa.getWorkTopics(json=json)

            if oa.getCitedByCount(json=json) < citedByMinimum:
                bar.next()
                continue

            if ptDF is None:
                bar.next()
                continue

            if (
                len(FIELD_FILTER.intersection(ptDF["field"]))
                < filterIntersection
            ):
                bar.next()
                continue
            else:
                dfs.append(row.copy().to_frame().T)
                bar.next()

        return pandas.concat(objs=dfs, ignore_index=True)


@click.command()
@click.option(
    "-e",
    "--email",
    "email",
    type=str,
    required=False,
    help="A valid email which will allow for access to the OpenAlex API Polite Pool",  # noqa: E501
    default=None,
)
@click.option(
    "-f",
    "--filter",
    "filter",
    required=False,
    type=click.Choice(choices=["field"]),
    help="Specify what paper attribute to filter on",
    default="field",
    show_default=True,
)
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    required=True,
    help="Path to a parquet file containing journal search results",
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
    ),
    required=True,
    help="Path to a parquet file to store papers that apply to the given filter",  # noqa: E501
)
@click.option(
    "--oa",
    "oaInputPath",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    required=False,
    help="OpenAlex search results to load",
    default=None,
    show_default=True,
)
@click.option(
    "--output-doi",
    "doiOutputPath",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
    ),
    required=True,
    help="Path to store the DOIs of all documents identified in the search",
)
@click.option(
    "--output-oa",
    "oaOutputPath",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
    ),
    required=True,
    help="Path to a parquet file to store OpenAlex results",
)
def main(
    doiOutputPath: Path,
    filter: str,
    inputPath: Path,
    oaOutputPath: Path,
    outputPath: Path,
    email: str | None = None,
    oaInputPath: Path | None = None,
) -> None:
    # 1. Check that files exist
    ifFileExistsExit(fps=[outputPath, oaOutputPath, doiOutputPath])

    # 2. Identify filter and relevant column
    filterTuple: Tuple[str, List[str]]
    match filter:
        case "field":
            filterTuple = ("field", FIELD_FILTER)
        case _:
            exit(1)

    # 3. Load search results
    print(f'Reading data from "{inputPath}"...')
    df: DataFrame = pandas.read_parquet(path=inputPath, engine="pyarrow")

    # 4. Extract DOIs from papers in the search result
    print("Extracting DOIs from search results...")
    source: Journal_ABC
    match df["journal"][0]:
        case "PLOS":
            source = PLOS()
        case _:
            exit(1)

    doisDF: DataFrame = extractDOIsFromHTML(source=source, df=df)

    # 5. Save DOI DataFrame
    print(f'Writing data to "{doiOutputPath}"...')
    doisDF.to_parquet(path=doiOutputPath, engine="pyarrow")

    # 6. Load OpenAlex search results if they exist
    oaDF: DataFrame
    if oaInputPath is not None:
        print(f'Reading data from "{oaInputPath}"...')
        oaDF = pandas.read_parquet(path=oaInputPath, engine="pyarrow")
    # 7. Get OpenAlex search results if they do not exist
    else:
        oaDF = getOpenAlexResults(df=doisDF, email=email)

        # 7a. Save OpenAlex DataFrame
        print(f'Writing data to "{oaOutputPath}"...')
        oaDF.to_parquet(path=oaOutputPath, engine="pyarrow")

    # 8. Filter documents based on field, subfield, or topic
    filteredDOIDF: DataFrame = filterOAResults(
        oaDF=oaDF,
        column=filterTuple[0],
        filterList=filterTuple[1],
    )

    # 9. Write filtered documents to file
    print(f'Writing data to "{outputPath}"...')
    filteredDOIDF.to_parquet(path=outputPath, engine="pyarrow")


if __name__ == "__main__":
    main()
