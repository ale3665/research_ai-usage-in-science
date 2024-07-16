from src.utils.search import SEARCH_QUERIES
import click
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from pyfs import isFile, resolvePath
import os
import re
import ast
import pandas as pd
import csv
from collections import Counter
from typing import List
import matplotlib.pyplot as plt
from progress.bar import Bar

def format_url(url: str) -> str:
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

def countKeywords(filePath: Path, queries: List[str]) -> List[str]:
    url: str = extractZettelInfo(filePath)

    keywordPatterns = [re.compile(k, re.IGNORECASE) for k in queries]
    
    results = []

    
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    content = response.text

    
    
    for pattern in keywordPatterns:
        keyword = pattern.pattern.strip('"').lower()
        count = len(pattern.findall(content))
        results.append(f"{keyword}: {count}")
    
    return results

def extractZettelInfo(filePath: Path) -> dict:
    """
    Extracts the URL information from a zettel file.

    This function reads the content of the zettel file located at `filePath`,
    and searches for a line starting with "url: ". It then extracts and returns
    the URL as a dictionary.

    :param filePath: The path to the zettel file.
    :type filePath: str
    :return: A dictionary containing the extracted URL with the key "url".
             If the URL is not found, the dictionary will be empty.
    :rtype: dict
    """
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.splitlines()
    for line in lines:
        if line.strip().startswith("url: "):
            url: str = line.strip().replace("url: ", "")
            return url
        
def plotKeywordCounts(df: pd.DataFrame):
    total_counts = {
        'deep learning': 0,
        'deep neural network': 0,
        'hugging face': 0,
        'huggingface': 0,
        'model checkpoint': 0,
        'model weights': 0,
        'pre-trained model': 0,
    }
    
    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        counts_str = row['search query counts']
        try:
            # Safely convert counts string to dictionary
            counts_dict = ast.literal_eval(counts_str)
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing counts string for row {index}: {counts_str}")
            continue
        
        # Accumulate counts for each keyword
        for key, value in counts_dict.items():
            total_counts[key.strip("'").lower()] += value
    
    # Extract DOIs for x-axis labels
    dois = df['url'].apply(lambda x: x.replace("doi.org/", ""))
    
    # Plotting the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(dois, [sum(total_counts.values())] * len(dois), color='skyblue')
    plt.xlabel('DOI')
    plt.ylabel('Total Count of Keywords')
    plt.title('Total Counts of Keywords in DOIs')
    plt.xticks(rotation=45, ha='right')
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
                url = extractZettelInfo(filePath)
                formatted_url = format_url(url)
                results.append((formatted_url, count))
            bar.next()
    
    df = pd.DataFrame(results, columns=['url', 'search query counts'])
    plotKeywordCounts(df)
    df.to_csv(csv, index=False, encoding='utf-8')



if __name__ == "__main__":
    main()
