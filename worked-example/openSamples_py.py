from webbrowser import open_new_tab

import pandas
from common import FILTERED_SAMPLE_FILENAME
from pandas import DataFrame


def main() -> None:
    df: DataFrame = pandas.read_json(path_or_buf=FILTERED_SAMPLE_FILENAME)

    doi: DataFrame
    for doi in df[df["ns"] == True]["doi"]:  # noqa: E712
        open_new_tab(url=doi)


if __name__ == "__main__":
    main()
