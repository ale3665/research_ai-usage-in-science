from src.utils.search import SEARCH_QUERIES
import click
from pathlib import Path

import seaborn as sns
from pyfs import resolvePath
import subprocess
import os

import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from progress.bar import Bar

def formatURL(url: str) -> str:
    """
    Formats a URL by removing the 'https://' prefix.

    :param url: The URL to format.
    :type url: str
    :return: The formatted URL without 'https://'.
    :rtype: str
    """
    return url.replace("https://", "")

def getDirectorySize(zettelDirectory: Path) -> int:
    """
    Counts the number of files in a directory.

    :param zettelDirectory: The directory path to count files from.
    :type zettelDirectory: Path
    :return: The number of files in the directory.
    :rtype: int
    """
    return sum(1 for _ in zettelDirectory.iterdir() if _.is_file())

def extractURL(filePath: Path) -> str:
    """
    Extracts the URL from a file based on a line starting with 'url: '.

    :param filePath: The path to the file containing the URL.
    :type filePath: Path
    :return: The extracted URL.
    :rtype: str
    """
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.splitlines()
    for line in lines:
        if line.strip().startswith("url: "):
            url: str = line.strip().replace("url: ", "")
            return url


def countKeywords(directory: str, keywords: List[str]) -> pd.DataFrame:
    """
    Counts occurrences of specified keywords in files within a directory using `grep`,
    and returns the results in a Pandas DataFrame.

    :param directory: Path to the directory containing files to search.
    :type directory: str
    :param keywords: List of keywords to search for in each file.
    :type keywords: List[str]
    :return: Pandas DataFrame with columns 'doi' (file name) and keyword counts.
    :rtype: pd.DataFrame
    """
    rows = []
    size = getDirectorySize(directory)
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    with Bar("Writing Open Alex tags to files...", max=size ) as bar:
        for filename in files:
            filepath = os.path.join(directory, filename)
            url = extractURL(filepath)
            doi = formatURL(url)
            counts = {keyword: 0 for keyword in keywords}
    
            for keyword in keywords:
                try:
                    result = subprocess.run(['grep', '-oF', keyword, filepath], capture_output=True, text=True)
                    counts[keyword] = len(result.stdout.splitlines())
                except subprocess.CalledProcessError as e:
                    counts[keyword] = 0

            counts['doi'] = doi
            rows.append(counts)
            bar.next()
        
    df = pd.DataFrame(rows)
    df = df[['doi'] + keywords]
    return df

def plot(df: pd.DataFrame):
    """
    Creates a bar plot of combined keyword counts for each DOI (URL) from the provided DataFrame.

    :param df: Pandas DataFrame containing 'doi' (URL) and keyword counts.
    :type df: pd.DataFrame
    :return: None
    """
    df['total count'] = df.drop(columns=['doi']).sum(axis=1)

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='doi', y='total count', data=df)

    ax.set_xlabel('DOI')
    ax.set_ylabel('Combined Keyword Counts')
    ax.set_title('Combined Keyword Counts for Each URL')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
     
    
    plt.tight_layout()
    plt.show()

@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a directory with zettels",
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    type=Path,
    required=True,
    help="Path to a csv file",
)
def main(inputPath: Path, outputPath: Path) -> None:
    """
    Main function to process zettel files, count keyword occurrences,
    plot the results, and save to a CSV file.

    :param inputPath: Path to the directory containing zettel files.
    :type inputPath: Path
    :param outputPath: Path to the output CSV file.
    :type outputPath: Path
    :return: None
    """
    queries: List[str] = SEARCH_QUERIES
    keywords = [keyword.replace('"', '') for keyword in queries]
    
    zettelDirectory: Path = resolvePath(path=inputPath)
    csv: Path = resolvePath(path=outputPath)

    df = (countKeywords(zettelDirectory, keywords))
    print(df)
    plot(df)
    df.to_csv(csv)




if __name__ == "__main__":
    main()
