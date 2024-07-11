from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


def parse_html(url: str):
    response = requests.get(url=url, timeout=60)
    if response.status_code == 200:
        soup = BeautifulSoup(markup=response.text, features="lxml")
        return soup
    else:
        print(f"Failed to retrieve page: {response.status_code}")


def dataToDict(soup):
    table = soup.find("table")
    df = pd.read_html(str(table))[0]
    df_selected = df[["ASJC category", "Subject area"]]
    grouped = (
        df_selected.groupby("Subject area")["ASJC category"]
        .apply(list)
        .to_dict()
    )

    return grouped


def save_dict_to_file(dictionary: dict[str, str], filename: Path):
    with open(filename, "w") as file:
        file.write("SCOPUS_SUBJECTS: dict[str, List[str]] = {\n")
        for key, values in dictionary.items():
            file.write(f'\t"{key}": [\n')
            for value in values:
                file.write(f'\t\t"{value}",\n')
            file.write("\t],\n")
        file.write("}")


def main() -> None:
    url: str = (
        "https://service.elsevier.com/app/answers/detail/a_id/15181/supporthub/scopus/"  # noqa: E501
    )
    soup: BeautifulSoup = parse_html(url)

    if soup:
        result_dict: dict[str, str] = dataToDict(soup)
        save_dict_to_file(result_dict, Path("output.txt"))


if __name__ == "__main__":
    main()
