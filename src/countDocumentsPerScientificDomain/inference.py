from pathlib import Path

import click
from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from src.countDocumentsPerScientificDomain.tokenizer import returnStr


@click.command()
@click.option("-i", "--input", "htmlFile", type=Path)
def main(htmlFile: Path) -> None:
    with open(file="./systemPrompt.txt", mode="r") as systemText:
        systemPrompt: str = systemText.read()
        systemText.close()

    prompt: str = returnStr(html=htmlFile)

    output_parser = StrOutputParser()

    chatPrompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [("system", systemPrompt), ("user", "{input}")]
    )

    llm: Ollama = Ollama(model="llama2")

    chain: RunnableSequence = chatPrompt | llm | output_parser

    print(chain.invoke({"input": prompt}))


if __name__ == "__main__":
    main()
