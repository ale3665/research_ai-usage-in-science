from string import Template
from typing import List, Literal, Protocol, runtime_checkable

SCIENCE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE: Template = Template(
    template="https://www.science.org/doi/pdf/${entryDOI}?download=true",
)
SCIENCE_JOURNAL_ENTRY_TAGS = [
    "Special Issue Research Article",
    "Research Article",
]
SCIENCE_JOURNAL_ENTRY_TAG_KEYS = ["dc_type"]

NATURE_JOURNAL_ENTRY_TAGS: None = None
NATURE_JOURNAL_ENTRY_TAGS_KEYS: List[str] = ["prism_publicationname"]
NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE: Template = Template(
    template="https://www.nature.com/articles/${entryDOI}.pdf"
)


def _partialDOI_Nature(doi: str) -> str:
    return doi.split("/")[1]


@runtime_checkable
class Journal(Protocol):
    name: str
    url: str
    feedType: Literal["api", "atom", "rss"]
    feedURL: str
    entryTags: List[str] | None
    entryTagKeys: List[str] | None
    entryDownloadURLTemplate: Template

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
        self.entryTags = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
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
        self.entryTags = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
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
        self.entryTags = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
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
        self.entryTags = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
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
        self.entryTags = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
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
        self.entryTags = SCIENCE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = SCIENCE_JOURNAL_ENTRY_TAG_KEYS
        self.entryDownloadURLTemplate: Template = (
            SCIENCE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE
        )

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(**kwargs)


class NatureActaPharmacologicaSinica(Journal):
    def __init__(self) -> None:
        self.name = "Nature Acta Pharmacologica Sinica"
        self.url = "https://www.nature.com/aps/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/aps.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureBDJInPractice(Journal):
    def __init__(self) -> None:
        self.name = "Nature BDJ In Practice"
        self.url = "https://www.nature.com/bdjinpractice/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/bdjinpractice.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureBDJOpen(Journal):
    def __init__(self) -> None:
        self.name = "Nature BDJ Open"
        self.url = "https://www.nature.com/bdjopen/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/bdjopen.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureBDJStudent(Journal):
    def __init__(self) -> None:
        self.name = "Nature BDJ Student"
        self.url = "https://www.nature.com/bdjstudent/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/bdjstudent.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureBDJTeam(Journal):
    def __init__(self) -> None:
        self.name = "Nature BDJ Team"
        self.url = "https://www.nature.com/bdjteam/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/bdjteam.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureBiopharmaDealmakers(Journal):
    def __init__(self) -> None:
        self.name = "Nature Biopharma Dealmakers"
        self.url = "https://www.nature.com/biopharmdeal/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/biopharmdeal.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureBJCReports(Journal):
    def __init__(self) -> None:
        self.name = "Nature BJC Reports"
        self.url = "https://www.nature.com/bjcreports/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/bjcreports.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureBloodCancerJournal(Journal):
    def __init__(self) -> None:
        self.name = "Nature Blood Cancer Journal"
        self.url = "https://www.nature.com/bcj/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/bcj.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureBoneMarrowTransplantation(Journal):
    def __init__(self) -> None:
        self.name = "Nature Bone Marrow Transplantation"
        self.url = "https://www.nature.com/bmt/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/bmt.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureBoneResearch(Journal):
    def __init__(self) -> None:
        self.name = "Nature Bone Research"
        self.url = "https://www.nature.com/boneres/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/boneres.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureBritishDentalJournal(Journal):
    def __init__(self) -> None:
        self.name = "Nature British Dental Journal"
        self.url = "https://www.nature.com/bdj/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/bdj.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureBritishJournalofCancer(Journal):
    def __init__(self) -> None:
        self.name = "Nature British Journal of Cancer"
        self.url = "https://www.nature.com/bjc/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/bjc.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCancerGeneTherapy(Journal):
    def __init__(self) -> None:
        self.name = "Nature Cancer Gene Therapy"
        self.url = "https://www.nature.com/cgt/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/cgt.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCellDeathAndDifferentiation(Journal):
    def __init__(self) -> None:
        self.name = "Nature Cell Death & Differentiation"
        self.url = "https://www.nature.com/cdd/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/cdd.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCellDeathAndDisease(Journal):
    def __init__(self) -> None:
        self.name = "Nature Cell Death & Disease"
        self.url = "https://www.nature.com/cddis/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/cddis.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCellDeathDiscovery(Journal):
    def __init__(self) -> None:
        self.name = "Nature Cell Death Discovery"
        self.url = "https://www.nature.com/cddiscovery/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/cddiscovery.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCellDiscovery(Journal):
    def __init__(self) -> None:
        self.name = "Nature Cell Discovery"
        self.url = "https://www.nature.com/celldisc/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/celldisc.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCellResearch(Journal):
    def __init__(self) -> None:
        self.name = "Nature Cell Research"
        self.url = "https://www.nature.com/cr/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/cr.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCellularAndMolecularImmunology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Cellular & Molecular Immunology"
        self.url = "https://www.nature.com/cmi/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/cmi.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCommunicationsBiology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Communications Biology"
        self.url = "https://www.nature.com/commsbio/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/commsbio.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCommunicationsChemistry(Journal):
    def __init__(self) -> None:
        self.name = "Nature Communications Chemistry"
        self.url = "https://www.nature.com/commschem/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/commschem.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCommunicationsEarthAndEnvironment(Journal):
    def __init__(self) -> None:
        self.name = "Nature Communications Earth & Environment"
        self.url = "https://www.nature.com/commsenv/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/commsenv.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCommunicationsEngineering(Journal):
    def __init__(self) -> None:
        self.name = "Nature Communications Engineering"
        self.url = "https://www.nature.com/commseng/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/commseng.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCommunicationsMaterials(Journal):
    def __init__(self) -> None:
        self.name = "Nature Communications Materials"
        self.url = "https://www.nature.com/commsmat/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/commsmat.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCommunicationsMedicine(Journal):
    def __init__(self) -> None:
        self.name = "Nature Communications Medicine"
        self.url = "https://www.nature.com/commsmed/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/commsmed.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCommunicationsPhysics(Journal):
    def __init__(self) -> None:
        self.name = "Nature Communications Physics"
        self.url = "https://www.nature.com/commsphys/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/commsphys.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureCommunicationsPsychology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Communications Psychology"
        self.url = "https://www.nature.com/commspsychol/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/commspsychol.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureEuropeanJournalofClinicalNutrition(Journal):
    def __init__(self) -> None:
        self.name = "Nature European Journal of Clinical Nutrition"
        self.url = "https://www.nature.com/ejcn/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ejcn.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureEuropeanJournalofHumanGenetics(Journal):
    def __init__(self) -> None:
        self.name = "Nature European Journal of Human Genetics"
        self.url = "https://www.nature.com/ejhg/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ejhg.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureEvidenceBasedDentistry(Journal):
    def __init__(self) -> None:
        self.name = "Nature Evidence-Based Dentistry"
        self.url = "https://www.nature.com/ebd/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ebd.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureExperimentalAndMolecularMedicine(Journal):
    def __init__(self) -> None:
        self.name = "Nature Experimental & Molecular Medicine"
        self.url = "https://www.nature.com/emm/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/emm.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureEye(Journal):
    def __init__(self) -> None:
        self.name = "Nature Eye"
        self.url = "https://www.nature.com/eye/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/eye.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureGeneTherapy(Journal):
    def __init__(self) -> None:
        self.name = "Nature Gene Therapy"
        self.url = "https://www.nature.com/gt/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/gt.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureGenesAndImmunity(Journal):
    def __init__(self) -> None:
        self.name = "Nature Genes & Immunity"
        self.url = "https://www.nature.com/gene/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/gene.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureHeredity(Journal):
    def __init__(self) -> None:
        self.name = "Nature Heredity"
        self.url = "https://www.nature.com/hdy/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/hdy.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureHumanGenomeVariation(Journal):
    def __init__(self) -> None:
        self.name = "Nature Human Genome Variation"
        self.url = "https://www.nature.com/hgv/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/hgv.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureHumanitiesandSocialSciencesCommunications(Journal):
    def __init__(self) -> None:
        self.name = "Nature Humanities and Social Sciences Communications"
        self.url = "https://www.nature.com/palcomms/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/palcomms.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureHypertensionResearch(Journal):
    def __init__(self) -> None:
        self.name = "Nature Hypertension Research"
        self.url = "https://www.nature.com/hr/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/hr.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureInternationalJournalofImpotenceResearch(Journal):
    def __init__(self) -> None:
        self.name = "Nature International Journal of Impotence Research"
        self.url = "https://www.nature.com/ijir/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ijir.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureInternationalJournalofObesity(Journal):
    def __init__(self) -> None:
        self.name = "Nature International Journal of Obesity"
        self.url = "https://www.nature.com/ijo/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ijo.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureInternationalJournalofObesitySupplements(Journal):
    def __init__(self) -> None:
        self.name = "Nature International Journal of Obesity Supplements"
        self.url = "https://www.nature.com/ijosup/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ijosup.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureInternationalJournalofOralScience(Journal):
    def __init__(self) -> None:
        self.name = "Nature International Journal of Oral Science"
        self.url = "https://www.nature.com/ijos/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ijos.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureISMECommunications(Journal):
    def __init__(self) -> None:
        self.name = "Nature ISME Communications"
        self.url = "https://www.nature.com/ismecomms/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ismecomms.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureTheISMEJournal(Journal):
    def __init__(self) -> None:
        self.name = "Nature The ISME Journal"
        self.url = "https://www.nature.com/ismej/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ismej.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureTheJournalofAntibiotics(Journal):
    def __init__(self) -> None:
        self.name = "Nature The Journal of Antibiotics"
        self.url = "https://www.nature.com/ja/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ja.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureJournalofExposureScienceAndEnvironmentalEpidemiology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Journal of Exposure Science & Environmental Epidemiology"
        self.url = "https://www.nature.com/jes/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/jes.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureJournalofHumanGenetics(Journal):
    def __init__(self) -> None:
        self.name = "Nature Journal of Human Genetics"
        self.url = "https://www.nature.com/jhg/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/jhg.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureJournalofHumanHypertension(Journal):
    def __init__(self) -> None:
        self.name = "Nature Journal of Human Hypertension"
        self.url = "https://www.nature.com/jhh/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/jhh.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureJournalofPerinatology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Journal of Perinatology"
        self.url = "https://www.nature.com/jp/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/jp.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureLabAnimal(Journal):
    def __init__(self) -> None:
        self.name = "Nature Lab Animal"
        self.url = "https://www.nature.com/laban/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/laban.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureLaboratoryInvestigation(Journal):
    def __init__(self) -> None:
        self.name = "Nature Laboratory Investigation"
        self.url = "https://www.nature.com/labinvest/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/labinvest.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureLeukemia(Journal):
    def __init__(self) -> None:
        self.name = "Nature Leukemia"
        self.url = "https://www.nature.com/leu/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/leu.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureLeukemiaSupplements(Journal):
    def __init__(self) -> None:
        self.name = "Nature Leukemia Supplements"
        self.url = "https://www.nature.com/leusup/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/leusup.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureLightScienceAndApplications(Journal):
    def __init__(self) -> None:
        self.name = "Nature Light: Science & Applications"
        self.url = "https://www.nature.com/lsa/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/lsa.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureMicrosystemsAndNanoengineering(Journal):
    def __init__(self) -> None:
        self.name = "Nature Microsystems & Nanoengineering"
        self.url = "https://www.nature.com/micronano/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/micronano.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureModernPathology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Modern Pathology"
        self.url = "https://www.nature.com/modpathol/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/modpathol.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureMolecularPsychiatry(Journal):
    def __init__(self) -> None:
        self.name = "Nature Molecular Psychiatry"
        self.url = "https://www.nature.com/mp/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/mp.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureMucosalImmunology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Mucosal Immunology"
        self.url = "https://www.nature.com/mi/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/mi.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNature(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature"
        self.url = "https://www.nature.com/nature/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nature.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureAfrica(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Africa"
        self.url = "https://www.nature.com/natafrica/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natafrica.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureAging(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Aging"
        self.url = "https://www.nature.com/nataging/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nataging.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureAstronomy(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Astronomy"
        self.url = "https://www.nature.com/natastron/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natastron.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureBiomedicalEngineering(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Biomedical Engineering"
        self.url = "https://www.nature.com/natbiomedeng/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natbiomedeng.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureBiotechnology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Biotechnology"
        self.url = "https://www.nature.com/nbt/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nbt.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureCancer(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Cancer"
        self.url = "https://www.nature.com/natcancer/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natcancer.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureCardiovascularResearch(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Cardiovascular Research"
        self.url = "https://www.nature.com/natcardiovascres/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natcardiovascres.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureCatalysis(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Catalysis"
        self.url = "https://www.nature.com/natcatal/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natcatal.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureCellBiology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Cell Biology"
        self.url = "https://www.nature.com/ncb/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ncb.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureChemicalBiology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Chemical Biology"
        self.url = "https://www.nature.com/nchembio/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nchembio.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureChemicalEngineering(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Chemical Engineering"
        self.url = "https://www.nature.com/natchemeng/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natchemeng.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureChemistry(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Chemistry"
        self.url = "https://www.nature.com/nchem/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nchem.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureCities(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Cities"
        self.url = "https://www.nature.com/natcities/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natcities.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureClimateChange(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Climate Change"
        self.url = "https://www.nature.com/nclimate/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nclimate.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureCommunications(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Communications"
        self.url = "https://www.nature.com/ncomms/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ncomms.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureComputationalScience(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Computational Science"
        self.url = "https://www.nature.com/natcomputsci/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natcomputsci.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureEcologyAndEvolution(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Ecology & Evolution"
        self.url = "https://www.nature.com/natecolevol/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natecolevol.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureElectronics(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Electronics"
        self.url = "https://www.nature.com/natelectron/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natelectron.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureEnergy(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Energy"
        self.url = "https://www.nature.com/nenergy/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nenergy.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureFood(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Food"
        self.url = "https://www.nature.com/natfood/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natfood.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureGenetics(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Genetics"
        self.url = "https://www.nature.com/ng/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ng.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureGeoscience(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Geoscience"
        self.url = "https://www.nature.com/ngeo/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ngeo.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureHumanBehaviour(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Human Behaviour"
        self.url = "https://www.nature.com/nathumbehav/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nathumbehav.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureImmunology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Immunology"
        self.url = "https://www.nature.com/ni/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/ni.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureIndia(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature India"
        self.url = "https://www.nature.com/natindia/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natindia.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureItaly(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Italy"
        self.url = "https://www.nature.com/natitaly/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natitaly.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureMachineIntelligence(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Machine Intelligence"
        self.url = "https://www.nature.com/natmachintell/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natmachintell.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureMaterials(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Materials"
        self.url = "https://www.nature.com/nmat/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nmat.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureMedicine(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Medicine"
        self.url = "https://www.nature.com/nm/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nm.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureMentalHealth(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Mental Health"
        self.url = "https://www.nature.com/natmentalhealth/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natmentalhealth.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureMetabolism(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Metabolism"
        self.url = "https://www.nature.com/natmetab/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natmetab.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureMethods(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Methods"
        self.url = "https://www.nature.com/nmeth/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nmeth.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureMicrobiology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Microbiology"
        self.url = "https://www.nature.com/nmicrobiol/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nmicrobiol.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureNanotechnology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Nanotechnology"
        self.url = "https://www.nature.com/nnano/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nnano.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureNeuroscience(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Neuroscience"
        self.url = "https://www.nature.com/neuro/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/neuro.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNaturePhotonics(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Photonics"
        self.url = "https://www.nature.com/nphoton/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nphoton.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNaturePhysics(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Physics"
        self.url = "https://www.nature.com/nphys/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nphys.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNaturePlants(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Plants"
        self.url = "https://www.nature.com/nplants/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nplants.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureProtocols(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Protocols"
        self.url = "https://www.nature.com/nprot/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nprot.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsBioengineering(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Bioengineering"
        self.url = "https://www.nature.com/natrevbioeng/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natrevbioeng.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsCancer(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Cancer"
        self.url = "https://www.nature.com/nrc/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrc.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsCardiology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Cardiology"
        self.url = "https://www.nature.com/nrcardio/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrcardio.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsChemistry(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Chemistry"
        self.url = "https://www.nature.com/natrevchem/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natrevchem.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsCleanTechnology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Clean Technology"
        self.url = "https://www.nature.com/nrct/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrct.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsClinicalOncology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Clinical Oncology"
        self.url = "https://www.nature.com/nrclinonc/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrclinonc.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsDiseasePrimers(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Disease Primers"
        self.url = "https://www.nature.com/nrdp/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrdp.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsDrugDiscovery(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Drug Discovery"
        self.url = "https://www.nature.com/nrd/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrd.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsEarthAndEnvironment(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Earth & Environment"
        self.url = "https://www.nature.com/natrevearthenviron/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natrevearthenviron.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsElectricalEngineering(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Electrical Engineering"
        self.url = "https://www.nature.com/natrevelectreng/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natrevelectreng.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsEndocrinology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Endocrinology"
        self.url = "https://www.nature.com/nrendo/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrendo.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsGastroenterologyAndHepatology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Gastroenterology & Hepatology"
        self.url = "https://www.nature.com/nrgastro/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrgastro.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsGenetics(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Genetics"
        self.url = "https://www.nature.com/nrg/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrg.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsImmunology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Immunology"
        self.url = "https://www.nature.com/nri/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nri.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsMaterials(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Materials"
        self.url = "https://www.nature.com/natrevmats/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natrevmats.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsMethodsPrimers(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Methods Primers"
        self.url = "https://www.nature.com/nrmp/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrmp.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsMicrobiology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Microbiology"
        self.url = "https://www.nature.com/nrmicro/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrmicro.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsMolecularCellBiology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Molecular Cell Biology"
        self.url = "https://www.nature.com/nrm/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrm.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsNephrology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Nephrology"
        self.url = "https://www.nature.com/nrneph/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrneph.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsNeurology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Neurology"
        self.url = "https://www.nature.com/nrneurol/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrneurol.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsNeuroscience(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Neuroscience"
        self.url = "https://www.nature.com/nrn/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrn.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsPhysics(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Physics"
        self.url = "https://www.nature.com/natrevphys/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natrevphys.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsPsychology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Psychology"
        self.url = "https://www.nature.com/nrpsychol/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrpsychol.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsRheumatology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Rheumatology"
        self.url = "https://www.nature.com/nrrheum/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrrheum.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureReviewsUrology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Reviews Urology"
        self.url = "https://www.nature.com/nrurol/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nrurol.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureStructuralAndMolecularBiology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Structural & Molecular Biology"
        self.url = "https://www.nature.com/nsmb/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nsmb.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureSustainability(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Sustainability"
        self.url = "https://www.nature.com/natsustain/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natsustain.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureSynthesis(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Synthesis"
        self.url = "https://www.nature.com/natsynth/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natsynth.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNatureWater(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nature Water"
        self.url = "https://www.nature.com/natwater/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/natwater.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNeuropsychopharmacology(Journal):
    def __init__(self) -> None:
        self.name = "Nature Neuropsychopharmacology"
        self.url = "https://www.nature.com/npp/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npp.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNPGAsiaMaterials(Journal):
    def __init__(self) -> None:
        self.name = "Nature NPG Asia Materials"
        self.url = "https://www.nature.com/am/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/am.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class Naturenpj2DMaterialsandApplications(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj 2D Materials and Applications"
        self.url = "https://www.nature.com/npj2dmaterials/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npj2dmaterials.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjAdvancedManufacturing(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Advanced Manufacturing"
        self.url = "https://www.nature.com/npjadvmanuf/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjadvmanuf.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjAging(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Aging"
        self.url = "https://www.nature.com/npjamd/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjamd.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjAntimicrobialsandResistance(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Antimicrobials and Resistance"
        self.url = "https://www.nature.com/npjamar/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjamar.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjBiodiversity(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Biodiversity"
        self.url = "https://www.nature.com/npjbiodivers/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjbiodivers.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjBiofilmsandMicrobiomes(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Biofilms and Microbiomes"
        self.url = "https://www.nature.com/npjbiofilms/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjbiofilms.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjBiologicalPhysicsandMechanics(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Biological Physics and Mechanics"
        self.url = "https://www.nature.com/npjbiolphysmech/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjbiolphysmech.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjBiologicalTimingandSleep(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Biological Timing and Sleep"
        self.url = "https://www.nature.com/npjbts/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjbts.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjBiosensing(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Biosensing"
        self.url = "https://www.nature.com/npjbiosensing/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjbiosensing.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjBreastCancer(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Breast Cancer"
        self.url = "https://www.nature.com/npjbcancer/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjbcancer.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjCardiovascularHealth(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Cardiovascular Health"
        self.url = "https://www.nature.com/npjcardiohealth/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjcardiohealth.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjCleanWater(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Clean Water"
        self.url = "https://www.nature.com/npjcleanwater/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjcleanwater.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjClimateAction(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Climate Action"
        self.url = "https://www.nature.com/npjclimataction/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjclimataction.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjClimateandAtmosphericScience(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Climate and Atmospheric Science"
        self.url = "https://www.nature.com/npjclimatsci/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjclimatsci.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjComplexity(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Complexity"
        self.url = "https://www.nature.com/npjcomplex/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjcomplex.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjComputationalMaterials(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Computational Materials"
        self.url = "https://www.nature.com/npjcompumats/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjcompumats.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjDigitalMedicine(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Digital Medicine"
        self.url = "https://www.nature.com/npjdigitalmed/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjdigitalmed.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjFlexibleElectronics(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Flexible Electronics"
        self.url = "https://www.nature.com/npjflexelectron/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjflexelectron.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjGenomicMedicine(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Genomic Medicine"
        self.url = "https://www.nature.com/npjgenmed/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjgenmed.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjGutandLiver(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Gut and Liver"
        self.url = "https://www.nature.com/npjgutliver/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjgutliver.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjImaging(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Imaging"
        self.url = "https://www.nature.com/npjimaging/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjimaging.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjMaterialsDegradation(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Materials Degradation"
        self.url = "https://www.nature.com/npjmatdeg/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjmatdeg.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjMaterialsSustainability(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Materials Sustainability"
        self.url = "https://www.nature.com/npjmatsustain/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjmatsustain.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjMentalHealthResearch(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Mental Health Research"
        self.url = "https://www.nature.com/npjmentalhealth/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjmentalhealth.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjMetabolicHealthandDisease(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Metabolic Health and Disease"
        self.url = "https://www.nature.com/npjmetabhealth/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjmetabhealth.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjMicrogravity(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Microgravity"
        self.url = "https://www.nature.com/npjmgrav/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjmgrav.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjNanophotonics(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Nanophotonics"
        self.url = "https://www.nature.com/npjnanophoton/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjnanophoton.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjNaturalHazards(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Natural Hazards"
        self.url = "https://www.nature.com/npjnathazards/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjnathazards.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjOceanSustainability(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Ocean Sustainability"
        self.url = "https://www.nature.com/npjoceansustain/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjoceansustain.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjParkinsonsDisease(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Parkinson's Disease"
        self.url = "https://www.nature.com/npjparkd/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjparkd.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjPrecisionOncology(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Precision Oncology"
        self.url = "https://www.nature.com/npjprecisiononcology/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjprecisiononcology.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjPrimaryCareRespiratoryMedicine(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Primary Care Respiratory Medicine"
        self.url = "https://www.nature.com/npjpcrm/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjpcrm.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjQuantumInformation(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Quantum Information"
        self.url = "https://www.nature.com/npjqi/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjqi.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjQuantumMaterials(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Quantum Materials"
        self.url = "https://www.nature.com/npjquantmats/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjquantmats.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjRegenerativeMedicine(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Regenerative Medicine"
        self.url = "https://www.nature.com/npjregenmed/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjregenmed.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjRobotics(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Robotics"
        self.url = "https://www.nature.com/npjrobot/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjrobot.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjScienceofFood(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Science of Food"
        self.url = "https://www.nature.com/npjscifood/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjscifood.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjScienceofLearning(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Science of Learning"
        self.url = "https://www.nature.com/npjscilearn/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjscilearn.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjSpintronics(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Spintronics"
        self.url = "https://www.nature.com/npjspintronics/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjspintronics.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjSustainableAgriculture(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Sustainable Agriculture"
        self.url = "https://www.nature.com/npjsustainagric/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjsustainagric.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjSustainableMobilityandTransport(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Sustainable Mobility and Transport"
        self.url = "https://www.nature.com/npjsustainmobil/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjsustainmobil.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjSystemsBiologyandApplications(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Systems Biology and Applications"
        self.url = "https://www.nature.com/npjsba/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjsba.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjUnconventionalComputing(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Unconventional Computing"
        self.url = "https://www.nature.com/npjunconvcomput/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjunconvcomput.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjUrbanSustainability(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Urban Sustainability"
        self.url = "https://www.nature.com/npjurbansustain/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjurbansustain.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjVaccines(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Vaccines"
        self.url = "https://www.nature.com/npjvaccines/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjvaccines.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjViruses(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Viruses"
        self.url = "https://www.nature.com/npjviruses/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjviruses.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturenpjWomensHealth(Journal):
    def __init__(self) -> None:
        self.name = "Nature npj Women's Health"
        self.url = "https://www.nature.com/npjwomenshealth/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjwomenshealth.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNPPDigitalPsychiatryandNeuroscience(Journal):
    def __init__(self) -> None:
        self.name = "Nature NPP\xe2\x80\x94Digital Psychiatry and Neuroscience"
        self.url = "https://www.nature.com/dpn/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/dpn.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureNutritionAndDiabetes(Journal):
    def __init__(self) -> None:
        self.name = "Nature Nutrition & Diabetes"
        self.url = "https://www.nature.com/nutd/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/nutd.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureOncogene(Journal):
    def __init__(self) -> None:
        self.name = "Nature Oncogene"
        self.url = "https://www.nature.com/onc/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/onc.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureOncogenesis(Journal):
    def __init__(self) -> None:
        self.name = "Nature Oncogenesis"
        self.url = "https://www.nature.com/oncsis/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/oncsis.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturePediatricResearch(Journal):
    def __init__(self) -> None:
        self.name = "Nature Pediatric Research"
        self.url = "https://www.nature.com/pr/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/pr.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureThePharmacogenomicsJournal(Journal):
    def __init__(self) -> None:
        self.name = "Nature The Pharmacogenomics Journal"
        self.url = "https://www.nature.com/tpj/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/tpj.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NaturePolymerJournal(Journal):
    def __init__(self) -> None:
        self.name = "Nature Polymer Journal"
        self.url = "https://www.nature.com/pj/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/pj.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureProstateCancerandProstaticDiseases(Journal):
    def __init__(self) -> None:
        self.name = "Nature Prostate Cancer and Prostatic Diseases"
        self.url = "https://www.nature.com/pcan/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/pcan.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureSchizophrenia(Journal):
    def __init__(self) -> None:
        self.name = "Nature Schizophrenia"
        self.url = "https://www.nature.com/npjschz/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/npjschz.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureScientificData(Journal):
    def __init__(self) -> None:
        self.name = "Nature Scientific Data"
        self.url = "https://www.nature.com/sdata/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/sdata.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureScientificReports(Journal):
    def __init__(self) -> None:
        self.name = "Nature Scientific Reports"
        self.url = "https://www.nature.com/srep/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/srep.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureSignalTransductionandTargetedTherapy(Journal):
    def __init__(self) -> None:
        self.name = "Nature Signal Transduction and Targeted Therapy"
        self.url = "https://www.nature.com/sigtrans/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/sigtrans.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureSpinalCord(Journal):
    def __init__(self) -> None:
        self.name = "Nature Spinal Cord"
        self.url = "https://www.nature.com/sc/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/sc.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureSpinalCordSeriesandCases(Journal):
    def __init__(self) -> None:
        self.name = "Nature Spinal Cord Series and Cases"
        self.url = "https://www.nature.com/scsandc/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/scsandc.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )


class NatureTranslationalPsychiatry(Journal):
    def __init__(self) -> None:
        self.name = "Nature Translational Psychiatry"
        self.url = "https://www.nature.com/tp/"
        self.feedType = "rss"
        self.feedURL = "https://www.nature.com/tp.rss"
        self.entryTags = NATURE_JOURNAL_ENTRY_TAGS
        self.entryTagKeys = NATURE_JOURNAL_ENTRY_TAGS_KEYS
        self.entryDownloadURLTemplate = NATURE_JOURNAL_ENTRY_DOWNLOAD_URL_TEMPLATE

    def entryDownloadURL(self, **kwargs) -> str:
        return self.entryDownloadURLTemplate.substitute(
            _partialDOI_Nature(doi=kwargs.get("entryDOI"))
        )
