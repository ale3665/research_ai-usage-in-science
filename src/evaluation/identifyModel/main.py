import pandas as pd

from pathlib import Path
from langchain.llms import Ollama



def identifyModel(filePath: Path):
    df = pd.read_parquet(filePath)

    ollama = Ollama(model="myModel")
    
    for title in df['titles']:
        
        prompt = f"""Return only the name of the machine learning model. If model name is identified, return as string, if not return n/a. The following are examples of identifying model names in titles.
                     STBLLM Breaking the 1-Bit Barrier with Structured Binary LLMs = STBLLM
                     Closing the gap between open-source and commercial large language models for medical evidence summarization = n/a
                     \n\n{title}"""
        response = ollama.run(prompt)
        print(f"Title: {title}\nResponse: {response}\n")
        # response = ollama.chat(model="myModel", messages=[
        #     {"role": "user", "content": f"""Return only the name of the machine learning model. If model name is identified, return as string, if not return n/a. The following are examples of identifying model names in titles.
        #      STBLLM Breaking the 1-Bit Barrier with Structured Binary LLMs = STBLLM
        #      Closing the gap between open-source and commercial large language models for medical evidence summarization = n/a
        #      \n\n{title}"""}
        # ])
        # print(f"Title: {title}\nResponse: {response}\n")


def main() -> None:
    filePath = "/Users/karolinaryzka/Documents/AIUS/research_ai-usage-in-science/data/plos/transformed_papers_08-12-2024.parquet"
    identifyModel(filePath)

if __name__ == "__main__":
    main()