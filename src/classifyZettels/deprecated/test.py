import pandas as pd
import subprocess
import os
from typing import List

SEARCH_QUERIES: List[str] = [
    r"Deep Learning",
    r"Deep Neural Network",
    r"Hugging Face",
    r"HuggingFace",
    r"Model Checkpoint",
    r"Model Weights",
    r"Pre-Trained Model",
]

def count_keywords_in_file(filepath: str, keywords: List[str]) -> pd.DataFrame:
    # Initialize a dictionary to store counts
    counts = {keyword: 0 for keyword in keywords}

    # Count occurrences of each keyword using grep
    for keyword in keywords:
        try:
            result = subprocess.run(['grep', '-oF', keyword, filepath], capture_output=True, text=True)
            counts[keyword] = len(result.stdout.splitlines())
        except subprocess.CalledProcessError as e:
            counts[keyword] = 0

    # Create a DataFrame with the results
    df = pd.DataFrame([counts])
    df.insert(0, 'file', filepath)
    
    return df

def count_keywords_in_directory(directory: str, keywords: List[str]) -> pd.DataFrame:
    # Initialize a dictionary to store counts
    rows = []
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for filename in files:
        filepath = os.path.join(directory, filename)

        counts = {keyword: 0 for keyword in keywords}
    
        for keyword in keywords:
            try:
                result = subprocess.run(['grep', '-oF', keyword, filepath], capture_output=True, text=True)
                counts[keyword] = len(result.stdout.splitlines())
            except subprocess.CalledProcessError as e:
                counts[keyword] = 0

        counts['doi'] = filename
        rows.append(counts)
        
    df = pd.DataFrame(rows)
    df = df[['doi'] + keywords]
    return df

# Example usage
filepath = '/Users/karolinaryzka/Documents/AIUS/research_ai-usage-in-science/src/classifyZettels/testZettels/10.1371_journal.pbio.2004285.yaml'
directory = '/Users/karolinaryzka/Documents/AIUS/research_ai-usage-in-science/src/classifyZettels/testZettels'
df = count_keywords_in_directory(directory, SEARCH_QUERIES)
print(df)
