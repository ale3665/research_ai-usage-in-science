from json import dump
from typing import List

from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, get


def getSoup() -> BeautifulSoup:
    resp: Response = get(url="https://www.nature.com/nature/browse-subjects")
    return BeautifulSoup(markup=resp.content, features="lxml")


def getPairingKeys(soup: BeautifulSoup) -> dict[str, List[str]]:
    data: dict[str, List[str]] = {}

    rs: ResultSet = soup.find_all(
        name="a",
        attrs={
            "data-track-action": "click-parent-subject",
        },
    )

    tag: Tag
    for tag in rs:
        data[tag.text.title()] = []

    return data


def getPairingValues(
    soup: BeautifulSoup, data: dict[str, List[str]]
) -> dict[str, List[str]]:
    keys: dict[str, str] = {
        key: "bar-" + key.lower().replace(" ", "-") for key in data.keys()
    }

    key: str
    subject: str
    for key, subject in keys.items():
        rs: ResultSet = soup.find_all(name="tr", attrs={"class": subject})

        tag: Tag
        for tag in rs:
            data[key].append(tag.find(name="a").text)

    return data


def main() -> None:
    soup: BeautifulSoup = getSoup()

    data: dict[str, List[str]] = getPairingKeys(soup=soup)
    data = getPairingValues(soup=soup, data=data)

    with open(file="nature_ScientificDomains.json", mode="w") as jsonFile:
        dump(obj=data, fp=jsonFile, indent=4)
        jsonFile.close()


if __name__ == "__main__":
    main()
