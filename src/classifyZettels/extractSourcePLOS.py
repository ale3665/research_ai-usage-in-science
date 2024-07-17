import requests
from bs4 import BeautifulSoup
from pathlib import Path
import csv
import os
from pyfs import resolvePath
import click

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

def extractDataLink(url: str):
    
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
                    dataLinks.append(tag['href'])
            
            if dataLinks:
                return dataLinks
            else:
                return ["Data links not found."]
        else:
            return ["Data Availability <strong> tag not found."]
    else:
        return [f"Failed to retrieve webpage. Status code: {response.status_code}"]
    
def linkToCSV (url: str, dataLinks, csvFile: Path):
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
def main(inputPath: Path, outputPath: Path) -> None:
    directory: Path = resolvePath(path=inputPath)
    csv: Path = resolvePath(path=outputPath)
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for filename in files:
        filepath = os.path.join(directory, filename)
        url = extractURL(filepath)
        dataLinks = extractDataLink(url)
        linkToCSV(url, dataLinks, csv)


if __name__ == "__main__":
    main()

