from abc import ABCMeta, abstractmethod


class Journal_ABC(metaclass=ABCMeta):
    """
    Journal_ABC _summary_

    _extended_summary_

    :param metaclass: _description_, defaults to ABCMeta
    :type metaclass: _type_, optional
    """

    @abstractmethod
    def search(self) -> None:
        pass

    @abstractmethod
    def extractPaperURLsFromSearchResult(self) -> None:
        pass

    @abstractmethod
    def extractDOIFromPaper(self) -> None:
        pass

    @abstractmethod
    def extractTitleFromPaper(self) -> None:
        pass

    @abstractmethod
    def extractAbstractFromPaper(self) -> None:
        pass

    @abstractmethod
    def extractContentFromPaper(self) -> None:
        pass

    @abstractmethod
    def createZettel(self) -> None:
        pass
