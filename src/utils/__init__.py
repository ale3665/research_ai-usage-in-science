import re
from os.path import isfile
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List


def ifFileExistsExit(fps: List[Path]) -> None:
    fp: Path
    for fp in fps:
        if isfile(path=fp):
            print(f'"{fp}" exists')
            exit(1)


def formatText(string: str) -> str:
    """
    Formats a given string by removing certain characters and cleaning up whitespace.

    This function performs the following operations on the input string:
    1. Removes hyphenated newlines (i.e., "-\n").
    2. Replaces newlines with an empty string.
    3. Collapses multiple spaces into a single space.

    :param string: The input string to be formatted.
    :type string: str
    :return: The formatted string with cleaned-up text.
    :rtype: str
    """  # noqa: E501
    string = re.sub(pattern=r"-\n", repl="", string=string)
    string = string.replace("\n", "")
    string = " ".join(string.split())
    return string


def storeStringInTempFile(string: str) -> str:
    """
    Stores a given string in a temporary file and returns the file's name.

    This function creates a temporary file, writes the given string to it,
    and returns the name of the temporary file. The temporary file is not
    deleted when closed, allowing the caller to access it later.

    :param string: The input string to be stored in the temporary file.
    :type string: str
    :return: The name of the temporary file containing the stored string.
    :rtype: str
    """
    tf: NamedTemporaryFile = NamedTemporaryFile(
        mode="w+t",
        delete=False,
    )

    tfName: str = tf.name

    tf.write(string)
    tf.close()

    return tfName
