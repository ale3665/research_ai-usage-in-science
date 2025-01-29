from os.path import abspath
from pathlib import Path

from sqlalchemy import (
    Column,
    Engine,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)


class DB:
    def __init__(self, fp: Path) -> None:
        self.fp: Path = Path(abspath(path=fp))
        self.engine: Engine = create_engine(url=f"sqlite:///{self.fp}")
        self.metadata: MetaData = MetaData()

    def createTables(self) -> None:
        years: Table = Table(
            "years",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("year", Integer, nullable=False),
        )

        keywords: Table = Table(
            "keywords",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("keyword", String, nullable=False),
        )

        journals: Table = Table(
            "journals",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("journal", String, nullable=False),
        )

        documents: Table = Table(
            "documents",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("doi", String, nullable=False),
        )

        searchResults: Table = Table(
            "search_results",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column(
                "document_id",
                Integer,
                ForeignKey("documents.id"),
                nullable=False,
            ),
            Column("response_id", Integer, nullable=False),
        )

        self.metadata.create_all(bind=self.engine, checkfirst=True)
