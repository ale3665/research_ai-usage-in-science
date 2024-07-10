import itertools
from itertools import chain

from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from src.classifyZettels import NATURE_SUBJECTS


def buildRunnableSequence(
    classifications: chain, model: str = "llama3"
) -> RunnableSequence:

    llm: Ollama = Ollama(model=model)

    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"Only return classifications. Only return one classification. Do not return markdown. Do not include astericks. Classify prompts as one of the following: {' '.join(classifications)}",  # noqa: E501
            ),
            ("user", "{input}"),
        ]
    )

    output: StrOutputParser = StrOutputParser()

    return prompt | llm | output


def main() -> None:
    topics: chain = itertools.chain.from_iterable(NATURE_SUBJECTS.values())
    # subjects: chain = itertools.chain.from_iterable(NATURE_SUBJECTS.keys())

    llmRunner: RunnableSequence = buildRunnableSequence(classifications=topics)
    output: str = llmRunner.invoke("Generate documentation for cash register")

    print(output)


if __name__ == "__main__":
    main()
