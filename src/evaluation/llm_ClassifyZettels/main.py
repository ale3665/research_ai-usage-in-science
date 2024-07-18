import itertools
from itertools import chain
from pathlib import Path
from sqlite3 import Connection, connect
from string import Template
from subprocess import PIPE, CompletedProcess, Popen  # nosec
from typing import Hashable, List, Tuple

import click
import pandas
from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence
from pandas import DataFrame, Series
from progress.bar import Bar
from pyfs import isFile, resolvePath

from src.llm_ClassifyZettels import NATURE_SUBJECTS, SCOPUS_SUBJECTS


def buildRunnableSequence(
    classifications: chain,
    ollamaModel: str,
) -> RunnableSequence:
    """
    Builds a runnable sequence for classifying prompts using a specified model.

    This function creates a runnable sequence that uses an Ollama model to classify
    input prompts. The sequence includes setting up a chat prompt template, configuring
    the language model, and defining an output parser. The classifications parameter
    specifies the possible classifications for the prompts.

    :param classifications: A chain of possible classifications to be used in the prompt.
    :type classifications: chain
    :param ollamaModel: The name of the Ollama model to be used for classification.
    :type ollamaModel: str
    :return: A runnable sequence configured for classifying prompts.
    :rtype: RunnableSequence
    """  # noqa: E501
    llm: Ollama = Ollama(model=ollamaModel)

    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"Only return classifications. Only return one classification. Do not return markdown. Do not include astericks. Use proper grammar. Classify prompts as one of the following: {' '.join(classifications)}",  # noqa: E501
            ),
            ("user", "{input}"),
        ]
    )

    output: StrOutputParser = StrOutputParser()
    return prompt | llm | output


def readDB(dbPath: Path) -> DataFrame:
    """
    Reads data from a database and returns it as a DataFrame.

    This function connects to a SQLite database at the specified path, executes
    a SQL query to retrieve data from the 'zettels' table, and returns the results
    as a Pandas DataFrame. The columns selected from the table are 'title', 'summary',
    and 'filename'.

    :param dbPath: The path to the SQLite database file.
    :type dbPath: Path
    :return: A DataFrame containing the retrieved data from the 'zettels' table.
    :rtype: DataFrame
    """  # noqa: E501
    sqlQuery: str = "SELECT title, summary, filename FROM zettels"
    conn: Connection = connect(database=dbPath)
    df: DataFrame = pandas.read_sql_query(sql=sqlQuery, con=conn)
    conn.close()
    return df


def inference(
    df: DataFrame,
    llmRunner: RunnableSequence,
    tagName: str,
    model: str,
) -> List[Tuple[int, str]]:
    """
    Perform inference on a DataFrame using a given LLM runner and return the results.

    This function iterates over each row in the provided DataFrame, constructs a
    prompt using the 'title' and 'summary' columns, and invokes the LLM runner to
    generate an output. The results are collected in a list of tuples, each containing
    the index of the row and the generated output tag.

    :param df: The DataFrame containing the data to be processed.
    :type df: DataFrame
    :param llmRunner: An instance of RunnableSequence used to perform the inference.
    :type llmRunner: RunnableSequence
    :param tagName: A tag name to be included in the output.
    :type tagName: str
    :param model: The name of the model to be included in the output.
    :type model: str
    :return: A list of tuples, each containing the index of the row and the generated output tag.
    :rtype: List[Tuple[int, str]]
    """  # noqa: E501
    data: List[Tuple[int, str]] = []

    with Bar("Inferencing data...", max=df.shape[0]) as bar:
        row: Series
        idx: Hashable
        for idx, row in df.iterrows():
            title: str = row["title"]
            abstract: str = row["summary"]
            prompt: str = f"title: {title} $$$ abstract: {abstract}"
            output: str = llmRunner.invoke(input=prompt)
            data.append((idx, model + "_" + tagName + "_" + output))
            bar.next()

    return data


def writeTagsToFile(data: List[Tuple[int, str]], filepaths: Series) -> None:
    """
    Writes tags to files based on the provided data and filepaths.

    This function iterates over a list of data tuples containing file indices and
    tags, constructs a command to append the tag to the corresponding file using
    a shell command, and executes the command. It uses a progress bar to indicate
    the progress of the operation.

    :param data: A list of tuples where each tuple contains an index and a tag.
    :type data: List[Tuple[int, str]]
    :param filepaths: A Series containing filepaths indexed by the same indices as in data.
    :type filepaths: Series
    :return: None
    """  # noqa: E501
    cmdTemplate: Template = Template(
        template='zettel --file ${filepath} --append-tag "${tag}" --in-place',
    )

    with Bar("Writing tags to files...", max=filepaths.size) as bar:
        datum: Tuple[int, str]
        for datum in data:
            fp: str = filepaths[datum[0]]

            cmd: str = cmdTemplate.substitute(filepath=fp, tag=datum[1])

            process: CompletedProcess = Popen(
                cmd,
                shell=True,
                stdout=PIPE,
            )  # nosec

            if process.returncode is not None:
                print(fp)

            bar.next()


@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to a Zettelgeist database",
)
@click.option(
    "-c",
    "--classes",
    "classificationName",
    type=click.Choice(
        [
            "nature-subjects",
            "nature-topics",
            "scopus-subjects",
            "scopus-topics",
        ]
    ),
    required=True,
    help="Classifications to use",
)
@click.option(
    "-m",
    "--model",
    "model",
    type=str,
    required=True,
    help="A valid Ollama model to utilize as a classifier",
)
def main(inputPath: Path, classificationName: str, model: str) -> None:
    """
    Main function to classify data and write tags to files.

    This function performs the following steps:
    1. Resolves the absolute input path and checks if it is a valid file.
    2. Reads the data from the specified database file into a DataFrame.
    3. Determines the classification scheme based on the classification name.
    4. Builds a runnable sequence using the specified model and classification scheme.
    5. Performs inference on the data to generate tags.
    6. Writes the generated tags to the corresponding files.

    :param inputPath: The path to the input database file.
    :type inputPath: Path
    :param classificationName: The name of the classification scheme to use.
    :type classificationName: str
    :param model: The name of the model to use for inference.
    :type model: str
    :return: None
    """  # noqa: E501
    absInputPath: Path = resolvePath(path=inputPath)

    if not isFile(path=absInputPath):
        print(f"{absInputPath} is not a file")
        exit(1)

    df: DataFrame = readDB(dbPath=absInputPath)

    classifications: chain
    match classificationName:
        case "nature-subjects":
            classifications = itertools.chain(NATURE_SUBJECTS.keys())
        case "nature-topics":
            classifications = itertools.chain.from_iterable(
                NATURE_SUBJECTS.values()
            )
        case "scopus-subjects":
            classifications = itertools.chain(SCOPUS_SUBJECTS.keys())
        case "scopus-topics":
            classifications = itertools.chain.from_iterable(
                SCOPUS_SUBJECTS.values()
            )
        case _:
            print("Invalid --classes option")
            exit(1)

    llmRunner: RunnableSequence = buildRunnableSequence(
        classifications=classifications,
        ollamaModel=model,
    )

    data: List[Tuple[int, str]] = inference(
        df=df,
        llmRunner=llmRunner,
        tagName=classificationName,
        model=model,
    )

    writeTagsToFile(data=data, filepaths=df["filename"])


if __name__ == "__main__":
    main()
