from sqlalchemy import Column, Date, MetaData, String, Table
from sqlalchemy.engine.base import Engine


def createSchema(engine: Engine) -> None:
    metadata: MetaData = MetaData()

    entries: Table = Table(
        "entries",
        metadata,
        Column("doi", String, primary_key=True),
        Column("url", String),
        Column("title", String),
        Column("source", String),
        Column("updated", Date),
    )

    metadata.create_all(bind=engine)
