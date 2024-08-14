import pandas
import ollama 
from pathlib import Path

def identifyModel(filePath: Path, output: Path):
    df = pandas.read_parquet(filePath)
    
    system_message = {
        "role": "system", 
        "content": f"""You are a pre-trained machine learning model identifier for academic papers. 
        Your task is to extract the names of pre-trained models from paper abstracts. 
        Return only the name of the identified model. If there are more than one, return them as a 
        numbered list. You keep responses concise without any extra information.
        input: Unlike recent language representation models, BERT is designed to pre-train deep bidirectional 
        representations from unlabeled text by jointly conditioning on both left and right context in all layers.
        As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create 
        state-of-the-art models for a wide range of tasks, such as question answering and language inference, without 
        substantial task-specific architecture modifications.
        output: BERT
        """
    }

    results = []
    max_iterations = 40

    for i, row in enumerate(df.itertuples(index=False)):
        if i >= max_iterations:
            break
        
        title = getattr(row, 'titles', 'n/a')  
        abstract = getattr(row, 'abstracts', 'n/a') 

        user_message = {
            "role": "user",
            "content": f"""From the following abstract, identify the names of machine learning models 
            and return the name. Do not identify machine learning techniques such as 'neural network model' 
            or 'principal component analysis'. If there are none, return 'n/a'.
            \n\n{abstract}"""
        }
        
        response = ollama.chat(model="myModel", messages=[system_message, user_message])
        content = response.get('message', {}).get('content', '').strip()

        if not content:
            content = 'n/a'

        results.append({"title": title, "response": content})

        #print(f"Title: {title}\nAbstract: {abstract}\nModel Identified: {content}\n")
    
    resultsDF = pandas.DataFrame(results)
    
    resultsDF.to_csv(output, index=False)

        


def main() -> None:
    filePath = "/Users/karolinaryzka/Documents/AIUS/research_ai-usage-in-science/data/plos/transformed_papers_08-12-2024.parquet"
    csvPath = "/Users/karolinaryzka/Documents/AIUS/research_ai-usage-in-science/src/evaluation/identifyModel/abTest.csv"
    identifyModel(filePath, csvPath)

if __name__ == "__main__":
    main()