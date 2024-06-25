from json import dump, dumps, load
from os.path import isfile
from pathlib import Path
from typing import List

import requests


def getJournals() -> dict:
    jsonFile: Path = Path("_fronteirsinJournalOptions.html")

    if isfile(jsonFile):
        with open(jsonFile, "r") as jf:
            return load(fp=jf)
    else:
        url = (
            "https://www.frontiersin.org/api/v3/journals/search/journal-filter"
        )

        payload = dumps(
            {
                "Skip": 0,
                "Top": 500,
                "DomainId": 0,
                "JournalIds": [],
                "Search": "",
                "FirstLetter": "",
            }
        )
        headers = {
            "Host": "www.frontiersin.org",
            "Content-Type": "application/json",
            "Cookie": "CurrentSessionId=1ba8da7a-1430-6876-1535-854c546db0ae",
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        jsonData: dict = response.json()

        with open(jsonFile, "w") as jf:
            dump(obj=jsonData, fp=jf)
            jf.close()

        return jsonData


def main() -> None:
    jsonData: dict = getJournals()
    journals: List[dict] = jsonData["Journals"]

    journal: dict
    for journal in journals:
        print(f'"{journal["AlternativeText"]}":"{journal["RSSUrl"]}",')


if __name__ == "__main__":
    main()
