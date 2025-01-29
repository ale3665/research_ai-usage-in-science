from itertools import product
from typing import List, Tuple

import pandas
from pandas import DataFrame

from src import SEARCH_KEYWORDS, YEARS
from src.db import DB
from src.journals.nature import Nature
from src.journals.plos import PLOS
from src.journals.science import Science
from src.types import SearchResultsDF


def _run(journal: Nature | PLOS) -> DataFrame:
    data: List[DataFrame] = []
    products: List[Tuple[str, int]] = list(
        product(
            SEARCH_KEYWORDS["keyword"].tolist(),
            YEARS["year"].tolist(),
        )
    )

    pair: Tuple[str, int]
    for pair in products:
        df: DataFrame = journal.searchJournal(query=pair[0], year=pair[1])
        data.append(df)

    df: DataFrame = pandas.concat(objs=data, ignore_index=True)

    SearchResultsDF(df_dict=df.to_dict(orient="records"))

    return df


def science() -> None:
    journal: Science = Science()
    journal.generateURLs(
        years=YEARS["year"].tolist(),
        queries=SEARCH_KEYWORDS["keyword"].tolist(),
    )
    print(journal.message)


def nature(db: DB) -> None:
    journal: Nature = Nature()
    df: DataFrame = _run(journal=journal)
    print(df)


def plos(db: DB) -> None:
    journal: PLOS = PLOS()
    df: DataFrame = _run(journal=journal)
    print(df)
