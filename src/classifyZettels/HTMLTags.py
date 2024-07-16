import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path

import click
from pyfs import isFile, resolvePath
from progress.bar import Bar

def getDirectorySize(zettelDirectory: Path) -> int:
    """
    Count the number of files in the given directory.

    :param directory: The path to the directory.
    :type directory: Path
    :return: The number of files in the directory.
    :rtype: int
    """
    return sum(1 for _ in zettelDirectory.iterdir() if _.is_file())

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
            url = line.strip().replace("url: ", "")
            return {
                "url": url,
            }

def getSubjectAreas(doiUrl: str) -> list:
    """
    Extracts subject areas from the provided DOI URL.

    This function sends a GET request to the provided DOI URL, parses the
    returned HTML content, and extracts subject areas listed under `li`
    elements that contain `a` elements with the class `taxo-term`.

    :param doi_url: The URL of the DOI page to retrieve subject areas from.
    :type doi_url: str
    :return: A list of subject areas extracted from the DOI page. If the request
             fails, it returns None and prints an error message.
    :rtype: list of str or None
    """

    response = requests.get(doiUrl)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        subjectAreas: list = []
        for li in soup.find_all('li'):
            term = li.find('a', class_='taxo-term')
            if term:
                subjectAreas.append(term.get_text().strip())
        
        return subjectAreas
    else:
        
        print(f"Failed to retrieve content from {doiUrl}. Status code: {response.status_code}")
        
def updateZettelFile(filePath: Path, subjects) -> None:
    """
    Appends subject areas to the zettel file.

    This function opens the specified zettel file in append mode and writes the
    provided list of subject areas to it. Each subject is written on a new line
    with an indentation. The subjects are prefixed with "HTML Subjects: " and
    followed by a separator line "---".

    :param filePath: The path to the zettel file to be updated.
    :type filePath: str
    :param subjects: A list of subject areas to be appended to the file.
    :type subjects: list of str
    :return: None
    """
    with open(filePath, 'a', encoding='utf-8') as file:
        subjects = subjects
        if subjects:
            file.write(f"HTML Subjects: \n")
        for topics in subjects:
            file.write(f"\t{topics}\n")
        file.write("---\n")

def processZettelFile(filePath: Path) -> None:
    """
    Processes a zettel file to extract the URL, search for subject areas, and update the file.

    This function performs the following steps:
    1. Extracts the URL from the zettel file.
    2. Searches for subject areas on the journal website using the extracted URL.
    3. Updates the zettel file with the found subject areas.

    :param filePath: The path to the zettel file to be processed.
    :type filePath: str
    :return: None
    """
    zettel: dict = extractZettelInfo(filePath)
    url: str = zettel["url"]
    print(f"Searching Journal for '{url}'...")
    subjects: list = getSubjectAreas(url)
    if subjects:
        updateZettelFile(filePath, subjects)
        print(f"Updated {filePath} with new data.")
    else:
        print(f"No HTML subjects found for '{url}'. Skipping update for {filePath}.")

@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a directory with Zettels",
)
def main(inputPath: Path) -> None:
    """
    Main function to process all zettel files in a specified directory.

    This function performs the following steps:
    1. Checks if the specified directory is valid.
    2. Iterates through all files in the directory.
    3. Processes each file using the `processZettelFile` function.

    :return: None
    """
    zettelDirectory: Path = resolvePath(path=inputPath)
    size = getDirectorySize(zettelDirectory)
    if not os.path.isdir(zettelDirectory):
        print(f"Error: '{zettelDirectory}' is not a valid directory.")

    with Bar("Writing HTML tags to files...", max=size) as bar:
        for filename in os.listdir(zettelDirectory):
            filePath: Path = os.path.join(zettelDirectory, filename)
            if os.path.isfile(filePath):
                processZettelFile(filePath)
            bar.next()

if __name__ == "__main__":
    main()
