from pathlib import Path
from sqlite3 import Connection, connect
from urllib.parse import urlparse
from pandas import DataFrame
import pandas
import requests
from pyfs import isFile, resolvePath
import click
from concurrent.futures import ThreadPoolExecutor, as_completed

def readDB(dbPath: Path) -> DataFrame:
    sqlQuery: str = "SELECT url, filename FROM zettels"
    conn: Connection = connect(database=dbPath)
    df: DataFrame = pandas.read_sql_query(sql=sqlQuery, con=conn)
    conn.close()
    return df

# def extractDataSource(url):
#     """
#     Extract the final data source (host) from a URL after following redirects.
    
#     Parameters:
#     url (str): The URL to extract the host from.
    
#     Returns:
#     str: The host of the final URL after redirects.
#     """
#     try:
#         response = requests.get(url)
#         final_url = response.url
#         parsed_url = urlparse(final_url)
#         return parsed_url.netloc
#     except requests.RequestException as e:
#         print(f"Failed to get the data source for URL {url}: {e}")
#         return None
    
def extractDataSource(url):
    """
    Extract the final data source (host) from a URL after following redirects.
    
    Parameters:
    url (str): The URL to extract the host from.
    
    Returns:
    str: The host of the final URL after redirects.
    """
    try:
        response = requests.get(url, timeout=10)  # Set a timeout of 10 seconds
        final_url = response.url
        return final_url
        # parsed_url = urlparse(final_url)
        # return parsed_url.netloc
    except requests.RequestException as e:
        print(f"Failed to get the data source for URL {url}: {e}")
        return None

def datasource(dbPath: Path) -> DataFrame:
    """
    Create a DataFrame with 'url' and 'datasource' columns.
    
    Parameters:
    dbPath (Path): Path to the database file.
    
    Returns:
    pd.DataFrame: DataFrame with 'url' and 'datasource' columns.
    """
    df = readDB(dbPath)
    df['datasource'] = df['url'].apply(extractDataSource)
    return df


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a Zettelgeist database",
)
@click.option(
    "-o",
    "--output",
    "outputPath",
    type=Path,
    required=True,
    help="Path to store data in CSV format",
)
def main(inputPath: Path, outputPath:Path) -> None:
    absInputPath: Path = resolvePath(path=inputPath)
    absOutputPath: Path = resolvePath(path=outputPath)

    df = datasource(absInputPath)
    df.to_csv(absOutputPath, index=False)

if __name__ == "__main__":
    main()