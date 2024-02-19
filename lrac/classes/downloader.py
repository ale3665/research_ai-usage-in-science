from pathlib import Path

from requests import Response, get


class PDFDownloader:
    def __init__(self) -> None:
        pass

    def download(self, url: str, doi: str, storageDirectory: Path) -> Path | None:
        """
        Downloads a PDF and saves it to a specific storageDirectory with the
        file pattern 'doi.pdf'.

        Forward slashes are replaced with $ signs for safety.
        """
        filepath: Path = Path(storageDirectory, f"{doi}.pdf")

        resp: Response = get(url=url)

        if resp.status_code == 200:
            with open(file=filepath, mode="wb") as pdfFile:
                pdfFile.write(resp.content)
                pdfFile.close()
            return filepath

        return None
