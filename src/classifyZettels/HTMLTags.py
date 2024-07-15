import os


def extractZettelInfo(filePath):
    """
    Extracts information from a zettel file located at the specified path.

    This function reads the content of the zettel file, extracts the url,
    and returns it as a dictionary.

    :param file_path: The path to the zettel file.
    :type file_path: str
    :return: A dictionary containing the extracted information.
             Returns {"url": extracted_url} if successful.
    :rtype: dict
    """
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()

    url = content.split('\n')[2].strip()
    url = url.replace("url: ", "")

    return {
        "url": url,
    }

def processZettelFile(filePath):
    zettel = extractZettelInfo


def main() -> None:
    directory = "/Users/karolinaryzka/Documents/AIUS/research_ai-usage-in-science/src/createZettels/zettels"
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")

    for filename in os.listdir(directory):
        filePath = os.path.join(directory, filename)
        if os.path.isfile(filePath):



if __name__ == "__main__":
    main()
