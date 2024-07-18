from src.utils.search import SEARCH_QUERIES
import click
from pathlib import Path
from bs4 import BeautifulSoup
import seaborn as sns
from pyfs import isFile, resolvePath
import os
import re
from matplotlib.ticker import MultipleLocator
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from progress.bar import Bar

def format_url(url: str) -> str:
    """
    Formats a URL by removing the 'https://' prefix if present.

    :param url: The URL to be formatted.
    :type url: str
    :return: The formatted URL without 'https://'.
    :rtype: str
    """
    return url.replace("https://", "")

def getDirectorySize(zettelDirectory: Path) -> int:
    """
    Count the number of files in the given directory.

    :param directory: The path to the directory.
    :type directory: Path
    :return: The number of files in the directory.
    :rtype: int
    """
    return sum(1 for _ in zettelDirectory.iterdir() if _.is_file())

def extractURL(filePath: Path) -> str:
    """
    Extracts the URL from a zettel file located at the specified file path.

    This function reads the content of the file line by line and searches for
    a line starting with 'url: '. If found, it extracts and returns the URL.

    :param filePath: The path to the zettel file.
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
        

def countKeywords(filePath: Path, queries: List[str]) -> List[str]:
    """
    Counts occurrences of specified keywords in a file.

    Reads the content of the file located at `filePath` and counts occurrences
    of each keyword in the `queries` list using case-insensitive matching.

    :param filePath: The path to the file to be searched.
    :type filePath: Path
    :param queries: A list of keywords to search for.
    :type queries: List[str] 
    :return: A list of strings showing keyword counts in the format "keyword: count".
    :rtype: List[str]
    """
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    keywordCounts = []
    for query in queries:
        pattern = re.compile(query, re.IGNORECASE)
        count = len(pattern.findall(content))
        keywordCounts.append(f"{query}: {count}")
    
    return keywordCounts

def parseKeywordCounts(counts_list: List[str]) -> int:
    """
    Parses keyword counts from a list of strings formatted as "keyword: count".

    Iterates through the `counts_list` and extracts counts for each keyword using
    regular expressions. Sums up all the counts and returns the total.

    :param counts_list: A list of strings formatted as "keyword: count".
    :type counts_list: List[str]
    :return: Total count of keywords extracted from the `counts_list`.
    :rtype: int
    """
    total = 0
    for count_str in counts_list:
        match = re.search(r': (\d+)', count_str)
        if match:
            total += int(match.group(1))
    
    return total
        
def plot(df: pd.DataFrame):
    """
    Plots a bar chart using Seaborn and Matplotlib based on keyword counts in the DataFrame.

    This function calculates combined keyword counts from 'search query counts' column 
    using `parseKeywordCounts`, and plots a bar chart with DOI on x-axis and combined 
    keyword counts on y-axis.

    :param df: DataFrame containing 'doi' and 'search query counts' columns.
    :type df: pd.DataFrame
    :return: None
    """
    df['combined counts'] = df['search query counts'].apply(parseKeywordCounts)

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='doi', y='combined counts', data=df)

    ax.set_xlabel('DOI')
    ax.set_ylabel('Combined Keyword Counts')
    ax.set_title('Combined Keyword Counts for Each URL')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_ylim(bottom=0)  
    ax.yaxis.set_major_locator(MultipleLocator(1))  
    
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
    Main function to process zettel files, count search queries, plot results, and save to CSV.

    This function iterates through zettel files in the specified input directory,
    counts occurrences of predefined search queries in each file, extracts URLs,
    formats them as DOIs, plots the combined keyword counts for each DOI using `plot`,
    and saves the results to a CSV file specified by `outputPath`.

    :param inputPath: Path to the directory containing zettel files.
    :type inputPath: Path
    :param outputPath: Path to the output CSV file where results will be saved.
    :type outputPath: Path
    :return: None
    """
    zettelDirectory: Path = resolvePath(path=inputPath)
    csv: Path = resolvePath(path=outputPath)
    size = getDirectorySize(zettelDirectory)
    queries: List[str] = SEARCH_QUERIES

    results: List = []

    with Bar("Counting search queries in Zettels...", max=size) as bar:
        for filename in os.listdir(zettelDirectory):
            filePath: Path = os.path.join(zettelDirectory, filename)
            if os.path.isfile(filePath):
                count = countKeywords(filePath, queries)
                url = extractURL(filePath)
                doi = format_url(url)
                results.append((doi, count))
            bar.next()
    
    df = pd.DataFrame(results, columns=['doi', 'search query counts'])
    
    plot(df)
    df.to_csv(csv, index=False, encoding='utf-8')



if __name__ == "__main__":
    main()
