from os.path import isfile
from typing import List

import pandas
from common import (
    FILENAME,
    FILTERED_SAMPLE_FILENAME,
    SAMPLED_FILENAME,
    saveDFToJSON,
)
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


def main() -> None:
    df: DataFrame
    if isfile(path=FILTERED_SAMPLE_FILENAME):
        df = pandas.read_json(path_or_buf=FILTERED_SAMPLE_FILENAME)

    else:
        json: DataFrame = pandas.read_json(path_or_buf=FILENAME)
        sampledDF: DataFrame = json.sample(
            frac=0.50,
            replace=False,
            random_state=42,
            ignore_index=True,
        )

        saveDFToJSON(df=sampledDF, filename=SAMPLED_FILENAME)

        df = filterWithOpenAlex(df=sampledDF)

        saveDFToJSON(df=df, filename=FILTERED_SAMPLE_FILENAME)

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
