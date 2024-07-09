# from typing import List

from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

# from src.classifyZettels import NATURE_SUBJECTS


def buildRunnableSequence(model: str = "llama3") -> RunnableSequence:

    llm: Ollama = Ollama(model=model)

    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a world class technical documentation writer.",
            ),
            ("user", "{input}"),
        ]
    )

    output: StrOutputParser = StrOutputParser()

    return prompt | llm | output


def main() -> None:
    chain: RunnableSequence = buildRunnableSequence()
    print(type(chain))


if __name__ == "__main__":
    main()
