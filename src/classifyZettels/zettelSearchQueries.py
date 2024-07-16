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
    
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.splitlines()
    for line in lines:
        if line.strip().startswith("url: "):
            url: str = line.strip().replace("url: ", "")
            return url
        

def countKeywords(filePath: Path, queries: List[str]) -> List[str]:
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    keywordCounts = []
    for query in queries:
        pattern = re.compile(query, re.IGNORECASE)
        count = len(pattern.findall(content))
        keywordCounts.append(f"{query}: {count}")
    
    return keywordCounts

def parseKeywordCounts(counts_list: List[str]) -> int:
    total = 0
    for count_str in counts_list:
        match = re.search(r': (\d+)', count_str)
        if match:
            total += int(match.group(1))
    
    return total
        
def plot(df: pd.DataFrame):
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
