from json import loads
from pathlib import Path
from time import sleep
from typing import List

import click
import pandas
from pandas import DataFrame, Series
from progress.bar import Bar
from pyfs import resolvePath
from requests import Response

from src.classes.journalGeneric import Journal_ABC
from src.classes.openalex import OpenAlex
from src.classes.plos import PLOS

# TODO: Add filter lists for subfields and topics
FIELD_FILTER: List[str] = [
    "Biological Sciences",
    "Agricultural and Biological Sciences",
    "Environmental Science",
    "Medicine",
    "Biochemistry, Genetics, and Molecular Biology",
    "Immunology and Microbiology",
    "Neuroscience",
    "Dentistry",
    "Health Professions",
    "Nursing",
    "Pharmacology, Toxicology, and Pharmaceutics",
    "Veterinary",
]


def getPaperDOIs(source: Journal_ABC, df: DataFrame) -> DataFrame:
    """
    Extract DOIs from paper URLs extracted from search results.

    This function takes in a Journal_ABC instance and a Pandas DataFrame containing search results.
    It uses the Journal_ABC instance to extract paper URLs from each search result,
    then extracts the DOI for each URL using the Journal_ABC instance's `extractDOIFromPaper` method.
    The resulting list of DOIs is returned as a Pandas DataFrame.

    :param source: An instance of the Journal_ABC class, used to extract paper URLs and DOIs.
    :type source: Journal_ABC
    :param df: A Pandas DataFrame containing search results from which to extract paper URLs.
    :type df: DataFrame
    :return: A Pandas DataFrame containing the extracted DOIs.
    :rtype: DataFrame
    """  # noqa: E501
    data: dict[str, List[str]] = {"urls": []}

    searchResultsHTML: Series = df["html"]

    with Bar(
        "Extracting paper URLs from search results...",
        max=searchResultsHTML.size,
    ) as bar:
        result: str
        for result in searchResultsHTML:
            urls: List[str] = source.extractPaperURLsFromSearchResult(
                respContent=result
            )
            data["urls"].extend(urls)
            bar.next()

        urlsDF: DataFrame = DataFrame(data=data)

        urlsDF["urls"] = urlsDF["urls"].apply(
            lambda x: f"https://doi.org/{source.extractDOIFromPaper(url=x)}"
        )

    return urlsDF


def getOpenAlexResults(df: DataFrame, email: str | None) -> DataFrame:
    """
    Retrieve OpenAlex metadata for a list of papers.

    This function takes in a Pandas DataFrame containing paper URLs and an optional email address.
    It uses the OpenAlex API to retrieve metadata for each paper, storing the results in a new DataFrame.
    The resulting DataFrame contains the DOI, API call URL, status code, and JSON response for each paper.

    :param df: A Pandas DataFrame containing paper URLs.
    :type df: DataFrame
    :param email: An optional email address used to authenticate with the OpenAlex API (if required).
    :type email: str | None
    :return: A new Pandas DataFrame containing the retrieved OpenAlex metadata for each paper.
    :rtype: DataFrame
    """  # noqa: E501
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
) -> DataFrame:
    """
    Filter OpenAlex results based on a list of fields.

    :param oaDF: The input DataFrame containing OpenAlex data.
    :type oaDF: pandas.DataFrame
    :param filterList: A list of fields to filter on.
    :type filterList: list[str]
    :param column: [NOT USED] (default is ..., indicating a required positional argument)
    :type column: str
    :return: The filtered DataFrame.
    :rtype: pandas.DataFrame

    Filtering is done by iterating over the input DataFrame, checking each row's primary topic field against the filter list. If the field matches, the corresponding document is added to the output.

    Example use cases:

        >>> from mymodule import filterOAResults
        >>> filtered_df = filterOAResults(oaDF, ["field1", "field2"])
    """  # noqa: E501
    dfs: List[DataFrame] = []

    df: DataFrame = oaDF[oaDF["status_code"] == 200].reset_index(drop=True)

    with Bar("Filtering academic papers...", max=df.shape[0]) as bar:
        row: Series
        for _, row in df.iterrows():
            oa: OpenAlex = OpenAlex()

            jsonStr: str = row["json"]
            json: dict = loads(s=jsonStr)

            ptDF: DataFrame | None = oa.getWorkPrimaryTopic(json=json)

            if ptDF is None:
                bar.next()
                continue

            if ptDF["field"].isin(filterList).any():
                dfs.append(row.copy().to_frame().T)
                bar.next()
            else:
                bar.next()

        return pandas.concat(objs=dfs, ignore_index=True)


@click.command()
@click.option(
    "-f",
    "--filter",
    "filter",
    required=False,
    type=click.Choice(choices=["field-biological_sciences"]),
    help="Filter to apply to papers",
    default="field-biological_sciences",
    show_default=True,
)
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
    "-i",
    "--load-search-results",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a parquet file containing journal search results",
)
@click.option(
    "--load-oa-results",
    "loadOA",
    type=Path,
    required=False,
    help="OpenAlex search results to load",
    default=None,
    show_default=True,
)
@click.option(
    "-o",
    "--output-filtered-papers",
    "outputPath",
    type=Path,
    required=True,
    help="Path to a parquet file to store papers that apply to the given filter",  # noqa: E501
)
@click.option(
    "--output-oa-results",
    "oaOutputPath",
    type=Path,
    required=True,
    help="Path to a parquet file to store OpenAlex results",
)
def main(
    inputPath: Path,
    oaOutputPath: Path,
    filter: str,
    outputPath: Path,
    email: str | None = None,
    loadOA: Path | None = None,
) -> None:
    """
    Load and filter journal search results using the OpenAlex API.

    This script loads a parquet file containing journal search results, gets OpenAlex
    search results for each DOIs found in the input file, filters the results based on the
    given filter is supported), and saves
    the filtered results to a new parquet file.

    :param inputPath: Path to a parquet file containing journal search results.
    :type inputPath: Path()
    :param oaOutputPath: Path to save OpenAlex results to.
    :type oaOutputPath: Path()
    :param filter: Filter to apply to papers.
    :type filter: str
    :param outputPath: Path to save filtered papers to.
    :type outputPath: Path()
    :param email: A valid email which will allow for access to the OpenAlex API Polite Pool. Defaults to None.
    :type email: str | None
    :param loadOA: Path to existing OpenAlex results. If provided, the script will use these results instead of getting new ones from the API. Defaults to None.
    :type loadOA: Path() | None
    """  # noqa: E501
    filteredDOIDF: DataFrame
    oaDF: DataFrame

    absInputPath: Path = resolvePath(path=inputPath)
    absOAOutputPath: Path = resolvePath(path=oaOutputPath)
    absOutputPath: Path = resolvePath(path=outputPath)

    if loadOA is None:
        df: DataFrame = pandas.read_parquet(
            path=absInputPath, engine="pyarrow"
        )
        journal: str = df["journal"][0]

        source: Journal_ABC
        match journal:
            case "PLOS":
                source = PLOS()
            case _:
                exit(1)

        doisDF: DataFrame = getPaperDOIs(source=source, df=df)

        oaDF = getOpenAlexResults(
            df=doisDF,
            email=email,
        )

        oaDF.to_parquet(path=absOAOutputPath, engine="pyarrow")

    else:
        absOAPath: Path = resolvePath(path=loadOA)

        oaDF = pandas.read_parquet(
            path=absOAPath,
            engine="pyarrow",
        )

    match filter:
        case "field-biological_sciences":
            filteredDOIDF = filterOAResults(
                oaDF=oaDF,
                filterList=FIELD_FILTER,
                column="field",
            )
        case _:
            exit(3)

    filteredDOIDF.to_parquet(path=absOutputPath, engine="pyarrow")


if __name__ == "__main__":
    main()
