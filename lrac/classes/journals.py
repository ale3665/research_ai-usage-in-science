from abc import ABCMeta, abstractmethod
from string import Template
from typing import List, Literal, Protocol, runtime_checkable

SCIENCE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE: Template = Template(
    template="https://www.science.org/doi/pdf/${entryDOI}?download=true",
)
SCIENCE_JOURNAL_ENTRY_TAGS: List[str] = ["Research Article"]
SCIENCE_JOURNAL_ENTRY_TAG_KEYS: List[str] = ["dc_type"]


@runtime_checkable
class Journal(Protocol):
    name: str
    url: str
    feedType: Literal["atom", "rss", "api"]
    feedURL: str
    entryTags: List[str]
    entryTagKeys: List[str]
    entryDownloadURLTemplate: Template

    @abstractmethod
    def entryDownloadURL(self, **kwargs) -> str:
        ...


class Science(Journal):
    def __init__(self) -> None:
        self.name = "Science"
        self.url = "https://www.science.org/journal/science"
        self.feedType = "rss"
        self.feedURL = (
            "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=science"
        )
        self.entryTags: List[str] = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys: List[str] = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
        self.entryDownloadURLTemplate: Template = (
            SCIENCE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE
        )

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(**kwargs)


class ScienceSignaling(Journal):
    def __init__(self) -> None:
        self.name: str = "Science Signaling"
        self.url: str = "https://www.science.org/journal/signaling"
        self.feedType = "rss"
        self.feedURL: str = (
            "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=signaling"
        )
        self.entryTags: List[str] = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys: List[str] = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
        self.entryDownloadURLTemplate: Template = (
            SCIENCE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE
        )

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(**kwargs)


class ScienceTranslationalMedicine(Journal):
    def __init__(self) -> None:
        self.name: str = "Science Translational Medicine"
        self.url: str = "https://www.science.org/journal/stm"
        self.feedType = "rss"
        self.feedURL: str = (
            "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=stm"
        )
        self.entryTags: List[str] = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys: List[str] = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
        self.entryDownloadURLTemplate: Template = (
            SCIENCE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE
        )

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(**kwargs)


class ScienceAdvances(Journal):
    def __init__(self) -> None:
        self.name: str = "Science Advances"
        self.url: str = "https://www.science.org/journal/sciadv"
        self.feedType = "rss"
        self.feedURL: str = (
            "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=sciadv"
        )
        self.entryTags: List[str] = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys: List[str] = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
        self.entryDownloadURLTemplate: Template = (
            SCIENCE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE
        )

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(**kwargs)


class ScienceImmunology(Journal):
    def __init__(self) -> None:
        self.name: str = "Science Immunology"
        self.url: str = "https://www.science.org/journal/sciimmunol"
        self.feedType = "rss"
        self.feedURL: str = (
            "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=sciimmunol"
        )
        self.entryTags: List[str] = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys: List[str] = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
        self.entryDownloadURLTemplate: Template = (
            SCIENCE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE
        )

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(**kwargs)


class ScienceRobotics(Journal):
    def __init__(self) -> None:
        self.name: str = "Science Robotics"
        self.url: str = "https://www.science.org/journal/scirobotics"
        self.feedType = "rss"
        self.feedURL: str = (
            "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=scirobotics"
        )
        self.entryTags: List[str] = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys: List[str] = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
        self.entryDownloadURLTemplate: Template = (
            SCIENCE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE
        )

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(**kwargs)
