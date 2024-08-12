import pandas
from common import FILENAME, SAMPLED_FILENAME, saveDFToJSON
from pandas import DataFrame
from progress.bar import Bar


def filterWithOpenAlex(df: DataFrame) -> None:
    with Bar("Filtering data through OpenAlex...", max=df.shape[0]) as bar:
        bar.next()
        pass


def main() -> None:
    json: DataFrame = pandas.read_json(path_or_buf=FILENAME)
    df: DataFrame = json.sample(
        n=100,
        replace=False,
        random_state=42,
        ignore_index=True,
    )

    saveDFToJSON(df=df, filename=SAMPLED_FILENAME)

    print(df)


if __name__ == "__main__":
    main()
