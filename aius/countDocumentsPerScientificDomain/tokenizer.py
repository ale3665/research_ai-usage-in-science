import re
from pathlib import Path
from typing import List

import click
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pyfs import resolvePath
from transformers import AutoTokenizer
from transformers.models.llama.tokenization_llama_fast import LlamaTokenizerFast


def readFile(path: Path) -> str:
    data: str = ""

    with open(file=path, mode="r") as htmlDoc:
        soup: BeautifulSoup = BeautifulSoup(markup=htmlDoc, features="lxml")
        data = (
            soup.find(
                name="div",
                attrs={"class": "c-article-body"},
            )
            .text.strip()
            .replace("\n", "")
            .replace("  ", " ")
        )
        htmlDoc.close()

    subData: str = re.sub(pattern=r" +", repl=" ", string=data)
    return subData


def removeStopWords(doc: str) -> str:
    tokens = word_tokenize(text=doc)
    stopTokens: set[str] = set(stopwords.words(fileids="english"))
    return " ".join([word for word in tokens if word.lower() not in stopTokens])


@click.command()
@click.option(
    "-i",
    "--input",
    "htmlFile",
    type=Path,
    required=True,
    help="Path to academic document stored as HTML file",
)
def main(htmlFile: Path) -> None:
    # nltk.download(info_or_id="punkt")
    # nltk.download(info_or_id="stopwords")

    htmlFile: Path = resolvePath(path=htmlFile)

    tokenizer: LlamaTokenizerFast = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path="meta-llama/Llama-2-7b-hf",
    )

    data: str = readFile(path=htmlFile)
    data = removeStopWords(doc=data)

    tokens: List[str] = tokenizer.tokenize(text=data)[0:4000]
    print(tokenizer.convert_tokens_to_string(tokens=tokens))


def returnStr(html: Path) -> str:
    # nltk.download(info_or_id="punkt")
    # nltk.download(info_or_id="stopwords")

    htmlFile: Path = resolvePath(path=html)

    tokenizer: LlamaTokenizerFast = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path="meta-llama/Llama-2-7b-hf",
    )

    data: str = readFile(path=htmlFile)
    data = removeStopWords(doc=data)

    tokens: List[str] = tokenizer.tokenize(text=data)[0:4000]
    return tokenizer.convert_tokens_to_string(tokens=tokens)


if __name__ == "__main__":
    main()
