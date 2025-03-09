import json
import logging
from pathlib import Path
from typing import List, Dict
import pandas as pd
from langdetect import detect

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate sentence pairs"""
    return df.drop_duplicates(subset=['bn', 'en'])

def filter_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """Apply quality filters"""
    mask = (
        (df['bn'].str.len() > 10) &
        (df['en'].str.len() > 10) &
        (df['bn'].str.len() < 1000) &
        (df['en'].str.len() < 1000)
    )
    return df[mask]

def main():
    logging.basicConfig(level=logging.INFO)
    data_dir = Path('data')
    
    # Load dataset
    df = pd.read_json(data_dir / 'dataset.json', lines=True)
    initial_size = len(df)
    
    # Apply maintenance
    df = remove_duplicates(df)
    df = filter_pairs(df)
    
    # Save cleaned dataset
    df.to_json(data_dir / 'dataset.json', orient='records', lines=True)
    logging.info(f"Removed {initial_size - len(df)} low quality pairs")

if __name__ == '__main__':
    main()
