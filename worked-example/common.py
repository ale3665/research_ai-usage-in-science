from pandas import DataFrame

FILENAME: str = "searchResponse_plos.json"
SAMPLED_FILENAME: str = "sampled_searchResponse_plos.json"
FILTERED_SAMPLE_FILENAME: str = "filter_sampled_searchResponse_plos.json"


def saveDFToJSON(df: DataFrame, filename: str) -> None:
    df.to_json(path_or_buf=FILENAME, index=False, indent=4)
