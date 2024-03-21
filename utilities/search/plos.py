from datetime import datetime
from string import Template
from typing import List
from webbrowser import open


def main() -> None:
    urlTemplate: Template = Template(
        template="https://journals.plos.org/plosone/search?filterStartDate=${year}-01-01&filterEndDate=${year}-12-31&resultsPerPage=60&q=${query}&sortOrder=DATE_NEWEST_FIRST&page=1",
    )
    queries: List[str] = [
        r'"Deep Learning"',
        r'"Deep Neural Network"',
        r'"Hugging Face"',
        r'"HuggingFace"',
        r'"Pre-Trained Model"',
    ]
    years: List[int] = list(range(2015, datetime.now().year + 1))

    query: str
    year: int
    for query in queries:
        for year in years:
            open(url=urlTemplate.substitute(query=query, year=year))


if __name__ == "__main__":
    main()
