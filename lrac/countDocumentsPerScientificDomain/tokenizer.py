from os import listdir
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
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
            .text.replace("\n", "")
            .replace("  ", " ")
        )
        htmlDoc.close()

    return data


def main() -> None:
    naturePath: Path = resolvePath(path=Path("../../data/nature/html/papers"))
    files: List[Path] = [Path(naturePath, f) for f in listdir(path=naturePath)]

    tokenizer: LlamaTokenizerFast = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path="meta-llama/Llama-2-7b-hf",
    )

    file: Path
    for file in files:
        data: str = readFile(path=file)
        tokens: List[str] = tokenizer.tokenize(text=data)[0:4000]
        print(repr(tokenizer.convert_tokens_to_string(tokens=tokens)))
        quit()


if __name__ == "__main__":
    main()
