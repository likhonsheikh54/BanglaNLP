import json
import logging
from pathlib import Path
from typing import Dict, List
import pandas as pd
from langdetect import detect

def validate_sentence_pair(bn_text: str, en_text: str) -> bool:
    """Validate Bengali-English sentence pair"""
    try:
        # Check language detection
        if detect(bn_text) != 'bn' or detect(en_text) != 'en':
            return False
            
        # Check length ratios
        bn_len = len(bn_text.split())
        en_len = len(en_text.split())
        if not (0.3 <= bn_len/en_len <= 3.0):
            return False
            
        return True
    except:
        return False

def validate_dataset(dataset_path: Path) -> Dict[str, List[str]]:
    """Validate entire dataset and return statistics"""
    errors = {
        'language': [],
        'length': [],
        'format': []
    }
    
    df = pd.read_json(dataset_path, lines=True)
    for idx, row in df.iterrows():
        if not validate_sentence_pair(row['bn'], row['en']):
            errors['language'].append(idx)
    
    return errors

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dataset_path = Path('data/dataset.json')
    
    errors = validate_dataset(dataset_path)
    total_errors = sum(len(e) for e in errors.values())
    
    if total_errors > 0:
        logging.error(f"Found {total_errors} validation errors")
        exit(1)
    else:
        logging.info("Dataset validation successful")
