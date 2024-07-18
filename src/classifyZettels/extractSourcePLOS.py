import requests
from bs4 import BeautifulSoup
from pathlib import Path
import csv
import os
from pyfs import resolvePath
import click
from typing import List, Optional

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

def extractZenodoDataLink(url: str) -> Optional[List[str]]:
    """
    Extract Zenodo data availability links from the given URL.

    This function sends a GET request to the provided URL, parses the HTML content,
    and extracts links that are related to data availability and hosted on Zenodo.

    :param url: The URL of the web page to extract data availability links from.
    :type url: str
    :return: A list of Zenodo data availability links, or None if no such links are found.
    :rtype: Optional[List[str]]
    """
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        strongTag = soup.find('strong', string='Data Availability: ')

        if strongTag:
            # Find all <a> tags after this <strong> tag until the next <strong> tag
            dataLinks = []
            for tag in strongTag.find_all_next():
                if tag.name == 'strong':
                    break
                if tag.name == 'a' and 'href' in tag.attrs:
                    if tag['href'].startswith('https') and 'zenodo' in tag['href']:
                        dataLinks.append(tag['href'])
            
            if dataLinks:
                return dataLinks
        return None         
    return None
    

def extractDataLink(url: str) -> List[str]:
    """
    Extract data availability links from the given URL.

    This function sends a GET request to the provided URL, parses the HTML content,
    and extracts links that are related to data availability.

    :param url: The URL of the web page to extract data availability links from.
    :type url: str
    :return: A list of data availability links or error messages.
    :rtype: List[str]
    """
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        strongTag = soup.find('strong', string='Data Availability: ')

        if strongTag:
            # Find all <a> tags after this <strong> tag until the next <strong> tag
            dataLinks = []
            for tag in strongTag.find_all_next():
                if tag.name == 'strong':
                    break
                if tag.name == 'a' and 'href' in tag.attrs:
                     if tag['href'].startswith('https'):
                        dataLinks.append(tag['href'])
                    #dataLinks.append(tag['href'])
            if dataLinks:
                return dataLinks
            else:
                return ["No data links found."]
        else:
            return ["Data Availability <strong> tag not found."]
    else:
        return [f"Failed to retrieve webpage. Status code: {response.status_code}"]
    

def linkToCSV (url, dataLinks, csvFile: Path) -> None:
    """
    Append the URL and its associated data links to a CSV file.

    :param url: The URL of the web page.
    :type url: str
    :param dataLinks: A list of data links extracted from the web page.
    :type dataLinks: List[str]
    :param csvFile: The path to the CSV file where the data should be written.
    :type csvFile: Path
    """
    joinedLinks = ', '.join(dataLinks)
    with open(csvFile, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the URL and joined data links to the CSV file
        writer.writerow([f"{url}: {joinedLinks}"])


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
@click.option(
    "-z",
    "--zenodoOutput",
    "zenodoOutputPath",
    type=Path,
    required=True,
    help="Path to a csv file",
)
def main(inputPath: Path, outputPath: Path, zenodoOutputPath:Path) -> None:
    """
    Process files in the specified directory, extract URLs, and extract data links from each URL.

    For each file in the input directory:
    1. Extracts the URL using `extractURL`.
    2. Extracts regular data links using `extractDataLink` and writes them to `outputPath`.
    3. Extracts Zenodo data links using `extractZenodoDataLink` and writes them to `zenodoOutputPath`
        if they exist.

    :param inputPath: Path to the directory containing files to process.
    :type inputPath: Path
    :param outputPath: Path to the CSV file where regular data links will be written.
    :type outputPath: Path
    :param zenodoOutputPath: Path to the CSV file where Zenodo data links will be written.
    :type zenodoOutputPath: Path
    :return: None
    """
    directory: Path = resolvePath(path=inputPath)
    csv1: Path = resolvePath(path=outputPath)
    csv2: Path = resolvePath(path=zenodoOutputPath)
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for filename in files:
        filepath = os.path.join(directory, filename)
        url = extractURL(filepath)
        dataLinks = extractDataLink(url)
        linkToCSV(url, dataLinks, csv1)
        zDataLinks = extractZenodoDataLink(url)
        if zDataLinks is not None:
            linkToCSV(url, zDataLinks, csv2)


if __name__ == "__main__":
    main()

