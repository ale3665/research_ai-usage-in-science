from pathlib import Path
from typing import List

import click
import pandas
from bs4 import BeautifulSoup
from pandas import DataFrame
from progress.bar import Bar
from pyfs import isDirectory, isFile, resolvePath
from zg.models.zettelDB import ZettelDB
from zg.zettel import Zettel, mergeZettelsToDF

from src.classes.journalGeneric import Journal_ABC
from src.classes.plos import PLOS


def extractContent(
    journal: Journal_ABC,
    df: DataFrame,
    outputDir: Path,
    numDocs: int = -1,
) -> List[Zettel]:
    """
    Extracts content from papers and creates Zettels.

    This function extracts DOIs, titles, abstracts, documents, notes, tags, and paths from the given DataFrame.
    It then uses these extracted elements to create Zettels, which are returned as a list.

    :param journal: The Journal interface for extracting DOI, title, abstract, document, note, tag, and path.
    :type journal: Journal_ABC
    :param df: The Pandas DataFrame containing the data to be processed.
    :type df: pandas.DataFrame
    :param outputDir: The directory where the extracted files will be saved.
    :type outputDir: Path
    :param numDocs: The maximum number of documents to process. Default is -1, which means all documents in the DataFrame.
    :type numDocs: int, optional
    :return: A list of Zettels created from the extracted content.
    :rtype: List[Zettel]
    """  # noqa: E501
    data: List[Zettel] = []

    dois: List[str] = []
    titles: List[str] = []
    abstracts: List[str] = []
    documents: List[str] = []
    notes: List[str] = []
    tags: List[List[str]] = []
    paths: List[Path] = []

    df: DataFrame = df[0:numDocs]

    with Bar("Extracting DOIs...", max=df.shape[0]) as bar:
        url: str
        for url in df["url"]:
            doi: str = journal.extractDOIFromPaper(url=url)
            dois.append(doi)

            fp: Path = Path(outputDir, doi.replace("/", "_") + ".yaml")
            paths.append(fp)

            bar.next()

    with Bar("Extracting HTML Content", max=df.shape[0]) as bar:
        html: bytes
        for html in df["html"]:
            soup: BeautifulSoup = BeautifulSoup(markup=html, features="lxml")

            titles.append(journal.extractTitleFromPaper(soup=soup))
            abstracts.append(journal.extractAbstractFromPaper(soup=soup))
            documents.append(journal.extractContentFromPaper(soup=soup))
            notes.append(journal.extractDataSourcesFromPaper(soup=soup))
            tags.append(journal.extractJournalTagsFromPaper(soup=soup))

            bar.next()

    with Bar("Creating Zettels...", max=df.shape[0]) as bar:
        idx: int
        for idx in range(df.shape[0]):
            zettel: Zettel = Zettel(
                document=documents[idx],
                filename=paths[idx],
                note=notes[idx],
                summary=abstracts[idx],
                title=titles[idx],
                url=f"https://doi.org/{dois[idx].replace('_', '/')}",
                tags=tags[idx],
            )

            data.append(zettel)

            bar.next()

    return data


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a journal's paper parquet file",
)
@click.option(
    "-o",
    "--output",
    "outputDir",
    type=Path,
    required=True,
    help="Directory to save Zettels to",
)
@click.option(
    "-n",
    "--number-of-documents",
    "numDocs",
    type=int,
    required=False,
    help="Number of documents to analyze. -1 means all documents are analyzed",  # noqa: E501
    default=-1,
    show_default=True,
)
def main(inputPath: Path, outputDir: Path, numDocs: int = -1) -> None:
    """
    main _summary_

    _extended_summary_

    :param inputPath: _description_
    :type inputPath: Path
    :param outputDir: _description_
    :type outputDir: Path
    :param numDocs: _description_, defaults to -1
    :type numDocs: int, optional
    """  # noqa: E501
    absInputPath: Path = resolvePath(path=inputPath)
    absOutputDirPath: Path = resolvePath(path=outputDir)

    if not isFile(path=absInputPath):
        print(f"{absInputPath} is not a file")
        exit(1)

    if not isDirectory(path=absOutputDirPath):
        print(f"{absOutputDirPath} is not a directory")
        exit(1)

    zdb: ZettelDB = ZettelDB(dbPath=Path(absOutputDirPath, "zettels.sqlite"))
    zdb.createTables()

    print(f"Reading {absInputPath} ...")
    df: DataFrame = pandas.read_parquet(path=absInputPath, engine="pyarrow")

    if numDocs < 0:
        numDocs = df.shape[0] + 1

    journalName: str = df["journal"][0]

    data: List[Zettel]
    match journalName:
        case "PLOS":
            journal: Journal_ABC = PLOS()
        case _:
            print("Unsupported journal")
            exit(1)

    data: List[Zettel] = extractContent(
        journal=journal,
        df=df,
        outputDir=absOutputDirPath,
        numDocs=numDocs,
    )

    zdf: DataFrame = mergeZettelsToDF(zettels=data)
    zdf["filename"] = zdf["filename"].apply(lambda x: x.__str__())
    zdf["tags"] = zdf["tags"].apply(lambda x: "✖️".join(x).replace('"', ""))

    zdf.to_sql(
        name="zettels",
        con=zdb.engine,
        index=True,
        index_label="id",
        if_exists="append",
    )


if __name__ == "__main__":
    main()
