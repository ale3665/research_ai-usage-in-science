from src.utils.search import SEARCH_QUERIES
import click
from pathlib import Path
from bs4 import BeautifulSoup
import seaborn as sns
from pyfs import resolvePath
import os
import re
from matplotlib.ticker import MultipleLocator
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from progress.bar import Bar

def formatURL(url: str) -> str:
    
    return url.replace("https://", "")

def getDirectorySize(zettelDirectory: Path) -> int:

    return sum(1 for _ in zettelDirectory.iterdir() if _.is_file())

def extractURL(filePath: Path) -> str:
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.splitlines()
    for line in lines:
        if line.strip().startswith("url: "):
            url: str = line.strip().replace("url: ", "")
            return url

def countKeywordsInDirectory(directory, keywords, size):
    
    data = []
    with Bar("Counting search queries in Zettels...", max=size) as bar:
        for filename in os.listdir(directory):
    
            filepath = os.path.join(directory, filename)
            
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            counts = {keyword: 0 for keyword in keywords}
            for keyword in keywords:
                counts[keyword] = len(re.findall(keyword, content, re.IGNORECASE))
            url = extractURL(filepath)
            doi = formatURL(url)
            row = {'doi': doi}
            row.update(counts)
            data.append(row)
            bar.next()

    
    df = pd.DataFrame(data)

    return df

        

def plot(df: pd.DataFrame):

    df['total count'] = df.drop(columns=['doi']).sum(axis=1)


    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='doi', y='total count', data=df)

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
    size: int = getDirectorySize(zettelDirectory)
    queries: List[str] = SEARCH_QUERIES

    df = (countKeywordsInDirectory(zettelDirectory, queries, size))
    print(df)
    plot(df)
    df.to_csv(csv)




if __name__ == "__main__":
    main()
