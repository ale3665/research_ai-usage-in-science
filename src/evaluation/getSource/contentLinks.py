from pathlib import Path
from typing import List
from urllib.parse import urlparse

import click
import pandas
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from progress.bar import Bar


def extractExternalLinks(htmlContent) -> List:
    soup = BeautifulSoup(htmlContent, "html.parser")
    articleText = soup.find("div", class_="article-text", id="artText")
    externalLinks = []

    if articleText:
        # content delineated by 'section _'
        sections = articleText.find_all(
            "div", id=lambda x: x and x.startswith("section")
        )

        for section in sections:
            # Find all <a> tags within each section
            links = section.find_all("a", href=True)
            for link in links:
                href = link["href"]
                parsed_href = urlparse(href)
                if parsed_href.netloc and parsed_href.netloc != "":
                    externalLinks.append(href)

    return externalLinks


def parseDoi(inputPath, outputPath: Path) -> None:
    df: DataFrame = pandas.read_parquet(inputPath)
    data = []
    bar = Bar("Processing Rows", max=len(df))
    for _, row in df.iterrows():
        doi = row["doi"]
        try:
            response = requests.get(doi, timeout=20)
            if response.status_code != 200:
                print(f"Failed to fetch the page at {doi}.")
                continue

            htmlContent = response.text
            links = extractExternalLinks(htmlContent)

            # doi label
            doi = doi.split("/")[-1]

            data.append([doi, "; ".join(links)])

        except Exception as e:
            print(f"An error occurred while processing {doi}: {e}")

        bar.next()
    bar.finish()
    df = pandas.DataFrame(data, columns=["DOI", "Links"])

    df.to_csv(outputPath, index=False, encoding="utf-8")
    print(f"Data successfully written to {outputPath}")


@click.command()
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
        path_type=Path,
    ),
    required=True,
    help="Path to a transformed set of papers",
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to a csv file",
)
def main(inputPath: Path, outputPath: Path) -> None:
    parseDoi(inputPath, outputPath)


if __name__ == "__main__":
    main()
