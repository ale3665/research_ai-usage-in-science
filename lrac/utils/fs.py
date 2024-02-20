from os import mkdir
from pathlib import Path


def createDirectory(directory: Path) -> None:
    try:
        mkdir(path=directory)
    except FileExistsError:
        pass
