import requests
from bs4 import BeautifulSoup
from pathlib import Path
import csv
import os

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

def extractDataLink(url):
    
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        strongTag = soup.find('strong', string='Data Availability: ')

        if strongTag:
            # Find the next <a> tag after this <strong> tag
            dataLink = strongTag.find_next('a', href=True)
            
            if dataLink:
                return dataLink['href']
            else:
                return "Data link not found."
        else:
            return "Data Availability <strong> tag not found."
    else:
        return f"Failed to retrieve webpage. Status code: {response.status_code}"
    
def linkToCSV (url, dataLink, csvFile):
    # Open the CSV file in append mode
    with open(csvFile, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the URL and data link to the CSV file
        writer.writerow([url, dataLink])

def main(directory: Path) -> None:
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for filename in files:
        filepath = os.path.join(directory, filename)
    url = extractURL()  # Replace with the actual URL
    dataLink = extractDataLink(url)
    

if __name__ == "__main__":
    main()

