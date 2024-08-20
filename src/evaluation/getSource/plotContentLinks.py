from pathlib import Path
from urllib.parse import urlparse

import click
import matplotlib.pyplot as plt
import pandas
import seaborn as sns


def plotBarValues(data: dict) -> None:
    for i, (_, value) in enumerate(zip(data.keys(), data.values())):
        plt.text(
            i,
            value + 0.25,
            str(int(value)),
            ha="center",
            color="black",
        )


def extract_domains(links: str) -> list:

    urls = links.split("; ")
    domains = []
    for url in urls:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain:
            domains.append(domain)
    return domains


def plot(input: str, output: str) -> None:
    df = pandas.read_csv(input)

    if "Links" not in df.columns:
        raise ValueError("The CSV file must contain a 'Links' column.")

    all_domains = df["Links"].apply(extract_domains).explode()
    domain_counts = all_domains.value_counts()

    top_domains = domain_counts.head(10).reset_index()
    top_domains.columns = ["Links", "Count"]

    plt.figure(figsize=(12, 8))

    sns.barplot(
        x="Links",
        y="Count",
        data=top_domains,
        palette="viridis",
        hue="Links",
        dodge=False,
    )

    plt.xlabel("Domain")
    plt.ylabel("Frequency")

    plotBarValues(top_domains.set_index("Links")["Count"].to_dict())

    plt.title("Top 10 Most Occurring Domains of External Paper Links")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output)
    plt.show()


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to a csv file of domains",
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to a png file of plots",
)
def main(inputPath: Path, outputPath: Path) -> None:
    plot(inputPath, outputPath)


if __name__ == "__main__":
    main()
