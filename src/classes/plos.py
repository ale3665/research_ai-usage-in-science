from string import Template

from src.classes.journalGeneric import Journal_ABC


class PLOS(Journal_ABC):
    def __init__(self) -> None:
        self.journalName: str = "PLOS"
        self.searchURLTemplate: Template = Template(
            template="https://journals.plos.org/plosone/dynamicSearch?filterStartDate=${year}-01-01&filterEndDate=${year}-12-31&resultsPerPage=100&q=${query}&sortOrder=DATE_NEWEST_FIRST&page=${page}&filterArticleTypes=Research Article"  # noqa: E501
        )
        pass

    def search(self) -> None:
        pass

    def extractPaperURLs(self) -> None:
        pass

    def downloadPapers(self) -> None:
        pass

    def extractDOIFromPaper(self) -> None:
        pass

    def extractTitleFromPaper(self) -> None:
        pass

    def extractAbstractFromPaper(self) -> None:
        pass

    def extractContentFromPaper(self) -> None:
        pass

    def createZettel(self) -> None:
        pass
