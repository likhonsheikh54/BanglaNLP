from pathlib import Path
import pandas as pd
from datasets import Dataset
from huggingface_hub import HfApi, upload_file
import os

def upload_dataset():
    # Load dataset
    df = pd.read_json('data/dataset.json', lines=True)
    dataset = Dataset.from_pandas(df)
    
    # Push to hub
    dataset.push_to_hub(
        "yourusername/bengali-english-news",
        token=os.environ['HF_TOKEN']
    )
    
    # Upload dataset card
    api = HfApi()
    api.upload_file(
        path_or_fileobj="dataset_card.md",
        path_in_repo="README.md",
        repo_id="yourusername/bengali-english-news",
        token=os.environ['HF_TOKEN']
    )

if __name__ == '__main__':
    upload_dataset()
