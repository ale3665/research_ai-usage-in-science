from pathlib import Path

from requests import Response, get


class PDFDownloader:
    def __init__(self) -> None:
        self.currentFilepath: Path | None = None
        self.currentResponse: Response | None = None
        self.currentURL: str | None = None

    def clear(self) -> None:
        self.currentFilepath = None
        self.currentResponse = None
        self.currentURL = None

    def download(self, url: str, doi: str, storageDirectory: Path) -> None:
        """
        Downloads a PDF and saves it to a specific storageDirectory with the
        file pattern 'doi.pdf'.

        Forward slashes are replaced with $ signs for safety.
        """
        self.currentURL = url
        self.currentFilepath = Path(storageDirectory, f"{doi}.pdf")
        self.currentResponse = get(url=self.currentURL)

        if self.currentResponse.status_code == 200:
            with open(file=self.currentFilepath, mode="wb") as pdfFile:
                pdfFile.write(self.currentResponse.content)
                pdfFile.close()
