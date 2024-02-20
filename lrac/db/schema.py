from sqlalchemy import Column, Date, MetaData, String, Table
from sqlalchemy.engine.base import Engine


def createSchema(engine: Engine) -> str:
    """
    Create the relevant tables and columns in a SQLite3 database and return the
    name of the table.
    """

    tableName: str = "entries"

    metadata: MetaData = MetaData()

    table: Table = Table(
        tableName,
        metadata,
        Column("doi", String, primary_key=True),
        Column("url", String),
        Column("title", String),
        Column("source", String),
        Column("updated", Date),
        Column("pdfFilename", String),
        Column("rssFilename", String),
    )

    metadata.create_all(bind=engine)

    return tableName
