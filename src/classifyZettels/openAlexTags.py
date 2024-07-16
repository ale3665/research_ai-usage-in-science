import requests
import os
from pathlib import Path

import click
from pyfs import resolvePath
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

def searchOpenAlex(workID: str) -> dict:
    """
    Search for work information in the OpenAlex API based on the work's ID.

    This function constructs a URL with the provided work ID and sends a GET request
    to the OpenAlex API to retrieve information about the work. It extracts the topic,
    field, and domain of the work from the API response.

    :param workID: The ID of the work to search for in the OpenAlex API.
    :type workID: str
    :return: A dictionary containing the topic, field, and domain of the work.
             Returns None if there is an error fetching data from OpenAlex.
    :rtype: dict or None
    """
    url = f"https://api.openalex.org/works/{workID}"
    headers = {
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        
        topic = data.get("primary_topic", {}).get("display_name", "N/A")
        field = data.get("primary_topic", {}).get("field", {}).get("display_name", "N/A")
        domain = data.get("primary_topic", {}).get("domain", {}).get("display_name", "N/A")
        
        return {
            "topic": topic,
            "field": field,
            "domain": domain
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from OpenAlex: {e}")
        return None


def getWorkId(title) -> str:
    """
    Retrieve the ID of a work based on a query using the OpenAlex API.

    This function constructs a URL with the provided query, sends a GET request
    to the OpenAlex API, and retrieves the ID of the first result if available.

    :param title: The query string used to search for the work in the OpenAlex API.
    :type title: str
    :return: The ID of the first work matching the query. Returns None if no results are found.
    :rtype: str or None
    """
    url = "https://api.openalex.org/works"
    params = {
        "search": title
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]['id']
    return None

def extractZettelInfo(filePath: Path) -> dict:
    """
    Extracts information from a zettel file located at the specified path.

    This function reads the content of the zettel file, extracts the title,
    and returns it as a dictionary.

    :param filePpath: The path to the zettel file.
    :type filePath: str
    :return: A dictionary containing the extracted information.
             Returns {"title": extracted_title} if successful.
    :rtype: dict
    """
    with open(filePath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    title_lines = []
    capturing_title = False

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("title: "):
            capturing_title = True
            title_lines.append(stripped_line.replace("title: ", ""))
        elif capturing_title:
            if stripped_line == "" or not line.startswith(" "):
                break
            title_lines.append(stripped_line)

    title = " ".join(title_lines)
    return {"title": title}

def updateZettelFile(filePath: Path, data: dict) -> None:
    """
    Updates a zettel file located at the specified path with new data.

    This function appends the topic, field, and domain information from `new_data`
    to the zettel file, separating each with a newline and ending with a delimiter.

    :param file_path: The path to the zettel file to be updated.
    :type filePath: str
    :param data: A dictionary containing new data to append to the zettel file.
                     Expected keys are 'topic', 'field', and 'domain'.
    :type data: dict
    :return: None
    """
    with open(filePath, 'a', encoding='utf-8') as file:
        file.write(f"OA topic: {data['topic']}\n")
        file.write(f"OA field: {data['field']}\n")
        file.write(f"OA domain: {data['domain']}\n")
        file.write("---\n")


def processZettelFile(filePath: Path) -> None:
    """
    Processes a zettel file by extracting information, searching for related work in the OpenAlex API,
    and updating the zettel file with the retrieved data if available.

    This function reads the zettel file located at `filePath`, extracts its title, searches for related work
    in the OpenAlex API using the title as a query, and updates the zettel file with information retrieved
    from the API if a work ID is found.

    :param filePath: The path to the zettel file to be processed.
    :type filePath: str
    :return: None
    """
    zettel: dict = extractZettelInfo(filePath)
    title: str = zettel["title"]
    print(f"\nSearching OpenAlex API for '{title}'...")
    workID: str = getWorkId(title)
    if workID:
        result: dict = searchOpenAlex(workID)
        if result:
            updateZettelFile(filePath, result)
            print(f"Updated {filePath} with new data.")
    else:
        print(f"No work ID found for '{title}'. Skipping update for {filePath}.")



@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a directory with zettels",
)
def main(inputPath: Path) -> None:
    """
    Processes each zettel file in the specified directory by updating it with relevant data
    retrieved from the OpenAlex API.

    This function iterates through each file in the directory specified by `directory`.
    For each file, it calls `processZettelFile(filePath)` to extract information, search
    for related work in the OpenAlex API, and update the file with retrieved data if available.

    :return: None
    """
    zettelDirectory: Path = resolvePath(path=inputPath)
    size = getDirectorySize(zettelDirectory)
    if not os.path.isdir(zettelDirectory):
        print(f"Error: '{zettelDirectory}' is not a valid directory.")

    with Bar("Writing Open Alex tags to files...", max=size) as bar:
        for filename in os.listdir(zettelDirectory):
            filePath: Path = os.path.join(zettelDirectory, filename)
            if os.path.isfile(filePath):
                processZettelFile(filePath)
            bar.next()
            
if __name__ == "__main__":
    main()

