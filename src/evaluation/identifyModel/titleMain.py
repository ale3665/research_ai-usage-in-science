import pandas
import ollama 
from pathlib import Path

def identifyModel(filePath: Path, output: Path):
    df = pandas.read_parquet(filePath)
    
    system_message = {
        "role": "system", 
        "content": f"""You are a pre-trained machine learning model identifier for academic papers. 
        Your task is to extract the names of pre-trained models from paper titles. 
        Return only the name of the identified model. If there are more than one, return them as a 
        numbered list. You keep responses concise without any extra information.
        input: BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
        output: BERT
        """
    }

    results = []
    max_iterations = 30

    for i, row in enumerate(df.itertuples(index=False)):
        if i >= max_iterations:
            break
        
        title = getattr(row, 'titles', 'n/a')  
        

        user_message = {
            "role": "user",
            "content": f"""From the following academic paper title, identify the names of machine learning models 
            and return the name. If there are none, return 'n/a'.
            \n\n{title}"""
        }
        
        response = ollama.chat(model="myModel", messages=[system_message, user_message])
        content = response.get('message', {}).get('content', '').strip()

        #many responses are coming back empty, showing something is wrongn n/a rather than 'n/a'
        if content and content != 'n/a':
            results.append({"title": title, "response": content})
        #responses can comeback empty (something went wrong)
        # if not content:
        #     content = 'empty'

        results.append({"title": title, "response": content})

        
    resultsDF = pandas.DataFrame(results)
    
    resultsDF.to_csv(output, index=False)

        


def main() -> None:
    filePath = "/Users/karolinaryzka/Documents/AIUS/research_ai-usage-in-science/data/plos/transformed_papers_08-12-2024.parquet"
    csvPath = "/Users/karolinaryzka/Documents/AIUS/research_ai-usage-in-science/src/evaluation/identifyModel/tiTest.csv"
    identifyModel(filePath, csvPath)

if __name__ == "__main__":
    main()