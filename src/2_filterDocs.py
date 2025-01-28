from json import dumps, loads
from pathlib import Path
from typing import List

import click
import pandas
from pandas import DataFrame, Series
from progress.bar import Bar

from src.filter import FIELD_FILTER
from src.utils import ifFileExistsExit

# 1. Only consider documents with at least one citation
# 2. Only consider documents that have at least two topics that are NS


def extractDocuments(df: DataFrame) -> DataFrame:
    data: dict[str, List[str | int | bool]] = {
        "doi": [],
        "json": [],
        "citations": [],
        "field_1": [],
        "field_2": [],
        "field_3": [],
        "ns": [],
    }

    field_1: str
    field_2: str
    field_3: str
    row: Series
    with Bar("Extracting documents...", max=df.shape[0]) as bar:
        for _, row in df.iterrows():
            json: dict = loads(s=row["json"])

            result: dict
            for result in json["results"]:
                ns: bool = False
                field_1, field_2, field_3 = ("", "", "")

                doi: str = result["doi"]
                citations: int = int(result["cited_by_count"])

                fieldCount: int = len(result["topics"])

                if fieldCount > 0:
                    field_1 = result["topics"][0]["field"]["display_name"]

                if fieldCount > 1:
                    field_2 = result["topics"][1]["field"]["display_name"]

                if fieldCount > 2:
                    field_3 = result["topics"][2]["field"]["display_name"]

                if (
                    len(
                        FIELD_FILTER.intersection(
                            [
                                field_1,
                                field_2,
                                field_3,
                            ]
                        )
                    )
                    > 2
                ):
                    ns = True

                jsonStr: str = dumps(obj=result)

                data["doi"].append(doi)
                data["json"].append(jsonStr)
                data["citations"].append(citations)
                data["field_1"].append(field_1)
                data["field_2"].append(field_2)
                data["field_3"].append(field_3)
                data["ns"].append(ns)

            bar.next()

    return DataFrame(data=data)


# def extractOACitedByCount(df: DataFrame) -> int:
#     jsonStr: str = df["json"][0]
#     jsonDict: dict = loads(s=jsonStr)
#     return jsonDict["cited_by_count"]


# def extractOATopicFields(df: DataFrame) -> List[str]:
#     data: List[str] = []

#     jsonStr: str = df["json"][0]
#     jsonDict: dict = loads(s=jsonStr)

#     topic: dict[str, str]
#     for topic in jsonDict["topics"]:
#         data.append(topic["field"]["display_name"])

#     return data


# def identifyIfNaturalScience(topics: List[str]) -> bool:
#     if len(FIELD_FILTER.intersection(topics)) < 2:
#         return False
#     return True


# def runner(df: DataFrame, email: str) -> DataFrame:
#     data: List[Series] = []

#     with Bar(
#         "Iterating through documents to find Natural Science documents...",
#         max=df.shape[0],
#     ) as bar:
#         row: Series
#         for _, row in df.iterrows():
#             resp: Response = getOA(email=email, doi=row["doi"])

#             oaDF: None | DataFrame = parseOAResponse(
#                 doi=row["doi"],
#                 resp=resp,
#             )

#             if oaDF is None:
#                 bar.next()
#                 continue

#             citedByCount: int = extractOACitedByCount(df=oaDF)

#             if citedByCount == 0:
#                 bar.next()
#                 continue

#             topics: List[str] = extractOATopicFields(df=oaDF)
#             if len(topics) < 2:
#                 bar.next()
#                 continue

#             isNaturalScienceDocument: bool = identifyIfNaturalScience(
#                 topics=topics,
#             )
#             if isNaturalScienceDocument:
#                 data.append(row.to_frame().T)

#             bar.next()

#     return pandas.concat(objs=data, ignore_index=True)


@click.command()
@click.option(
    "-i",
    "--input",
    "inputFP",
    required=True,
    help="OpenAlex query file",
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "-o",
    "--output",
    "outputFP",
    required=True,
    help="Apache Parquet file to write Natrual Science documents",
    type=click.Path(
        exists=False,
        file_okay=True,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
def main(inputFP: Path, outputFP: Path) -> None:
    ifFileExistsExit(fps=[outputFP])

    df: DataFrame = pandas.read_parquet(path=inputFP, engine="pyarrow")

    docs: DataFrame = extractDocuments(df=df)
    docs.to_parquet(path=outputFP, engine="pyarrow")


if __name__ == "__main__":
    main()
