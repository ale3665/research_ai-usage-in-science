import pandas
import ollama 
from pathlib import Path

def identifyModel(filePath: Path, output: Path):
    df = pandas.read_parquet(filePath)
    
    system_message = {
        "role": "system", 
        "content": f"""You are a pre-trained machine learning model identifier for academic papers. 
        Your task is to extract the names of pre-trained models from paper content. 
        Return only the name of the identified model. If there are more than one, return them as a 
        numbered list. You keep responses concise without any extra information."""
    }

    results = []
    max_iterations = 5

    for i, row in enumerate(df.itertuples(index=False)):
        if i >= max_iterations:
            break
        
        title = getattr(row, 'titles', 'n/a')  
        content = getattr(row, 'content', 'n/a') 

        user_message = {
            "role": "user",
            "content": f"""From the following academic paper content, identify the names of machine learning models 
            and return the name. Only list the model names, not the authors, references or other content. If there are none, return 'n/a'. I will provide an example.
            input: 'SVM [42] is a discriminative classification algorithm which is able to find a decision hyper-plane with the maximum distance 
            (margin) to the nearest data points (Support Vectors) of each class. As a result, this method has a high generalization power. '
            output: SVM
            \n\n{content}"""
        }
        
        response = ollama.chat(model="myModel", messages=[system_message, user_message])
        answer = response.get('message', {}).get('content', '').strip()

        if not answer:
            answer = 'n/a'

        results.append({"title": title, "response": answer})

        #print(f"Title: {title}\nAbstract: {abstract}\nModel Identified: {content}\n")
    
    resultsDF = pandas.DataFrame(results)
    
    resultsDF.to_csv(output, index=False)

        


def main() -> None:
    filePath = "/Users/karolinaryzka/Documents/AIUS/research_ai-usage-in-science/data/plos/transformed_papers_08-12-2024.parquet"
    csvPath = "/Users/karolinaryzka/Documents/AIUS/research_ai-usage-in-science/src/evaluation/identifyModel/coTest.csv"
    identifyModel(filePath, csvPath)

if __name__ == "__main__":
    main()