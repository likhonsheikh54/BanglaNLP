from typing import List, Dict, Tuple, Optional
import json
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from collections import Counter
from tqdm import tqdm
from datasets import Dataset, DatasetDict
from langdetect import detect, LangDetectException

class DatasetBuilder:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dataset_path = self.output_dir / 'dataset.json'
        self.stats = Counter()  # For tracking statistics
        
    def add_article_pair(self, bn_article: Dict, en_article: Dict):
        """Add a Bengali-English article pair to the dataset"""
        aligned_pairs = self._align_paragraphs(
            bn_article['content'],
            en_article['content']
        )
        
        if aligned_pairs:
            # Save aligned pairs
            pair_id = self._generate_pair_id(bn_article['url'])
            self._save_pair(pair_id, aligned_pairs, 
                          bn_article['url'], en_article['url'])
            self.stats[bn_article['url'].split('/')[2]] += len(aligned_pairs)
            return len(aligned_pairs)
        return 0
    
    def build_huggingface_dataset(self) -> str:
        """Convert saved pairs to HuggingFace dataset format with filtering"""
        logging.info("Building dataset from saved pairs...")
        pairs = []
        pair_files = list(self.output_dir.glob('*.json'))
        logging.info(f"Found {len(pair_files)} article pair files")
        
        for f in tqdm(pair_files, desc="Processing pairs"):
            with open(f) as fp:
                try:
                    pair_data = json.load(fp)
                    for bn, en in pair_data['pairs']:
                        pairs.append({
                            'bn': bn,
                            'en': en,
                            'source': pair_data.get('source', 'unknown'),
                            'url': pair_data.get('bn_url', ''),
                            'date': pair_data.get('date', '')
                        })
                except json.JSONDecodeError:
                    logging.warning(f"Failed to parse {f}")
        
        logging.info(f"Total pairs before filtering: {len(pairs)}")
        
        # Apply quality filters
        filtered_pairs = self._apply_quality_filters(pairs)
        logging.info(f"Total pairs after filtering: {len(filtered_pairs)}")
        
        # Save as JSON lines
        df = pd.DataFrame(filtered_pairs)
        df.to_json(self.dataset_path, orient='records', lines=True)
        
        # Create train-test-validation split
        self._create_splits(df)
        
        return str(self.dataset_path)
    
    def upload_to_huggingface(self, repo_id: str):
        """Upload dataset to Hugging Face Hub"""
        try:
            from huggingface_hub import HfApi
            from datasets import load_dataset
            
            # Convert to Hugging Face Dataset
            logging.info("Converting to Hugging Face dataset format...")
            dataset = load_dataset('json', data_files={
                'train': str(self.output_dir / 'train.json'),
                'validation': str(self.output_dir / 'validation.json'),
                'test': str(self.output_dir / 'test.json')
            })
            
            # Push to Hub
            logging.info(f"Pushing to Hugging Face Hub: {repo_id}")
            dataset.push_to_hub(repo_id)
            
            # Also upload dataset card if it exists
            api = HfApi()
            dataset_card_path = Path('../dataset_card.md')
            if dataset_card_path.exists():
                api.upload_file(
                    path_or_fileobj=str(dataset_card_path),
                    path_in_repo="README.md",
                    repo_id=repo_id
                )
                logging.info("Uploaded dataset card")
                
            logging.info(f"Dataset uploaded to: https://huggingface.co/datasets/{repo_id}")
            return True
        except Exception as e:
            logging.error(f"Error uploading to Hugging Face: {str(e)}")
            return False

    def _apply_quality_filters(self, pairs: List[Dict]) -> List[Dict]:
        """Apply quality filters to remove bad pairs"""
        logging.info("Applying quality filters...")
        filtered = []
        
        for pair in tqdm(pairs, desc="Filtering"):
            bn, en = pair['bn'], pair['en']
            
            # Check minimum length
            if len(bn) < 20 or len(en) < 20:
                continue
                
            # Check length ratio (Bengali to English)
            ratio = len(bn) / len(en) if len(en) > 0 else 0
            if not (0.5 <= ratio <= 3.0):
                continue
                
            # Verify language if possible
            try:
                bn_lang = detect(bn)
                en_lang = detect(en)
                if not (bn_lang == 'bn' and en_lang == 'en'):
                    continue
            except LangDetectException:
                # If language detection fails, keep the pair
                pass
                
            filtered.append(pair)
            
        return filtered
    
    def _create_splits(self, df: pd.DataFrame):
        """Create train-test-validation splits"""
        # Shuffle dataframe
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Create splits (80% train, 10% validation, 10% test)
        train_size = int(0.8 * len(df))
        val_size = int(0.1 * len(df))
        
        train_df = df[:train_size]
        val_df = df[train_size:train_size+val_size]
        test_df = df[train_size+val_size:]
        
        # Save splits
        train_df.to_json(self.output_dir / 'train.json', orient='records', lines=True)
        val_df.to_json(self.output_dir / 'validation.json', orient='records', lines=True)
        test_df.to_json(self.output_dir / 'test.json', orient='records', lines=True)
        
        logging.info(f"Created splits: train={len(train_df)}, val={len(val_df)}, test={len(test_df)}")

    def _generate_pair_id(self, url: str) -> str:
        """Generate unique ID for article pair"""
        import hashlib
        return hashlib.md5(url.encode()).hexdigest()
        
    def _save_pair(self, pair_id: str, pairs: List[Tuple[str, str]], 
                   bn_url: str, en_url: str, date: str = ''):
        """Save aligned sentence pairs to JSON"""
        data = {
            'id': pair_id,
            'bn_url': bn_url,
            'en_url': en_url,
            'pairs': pairs,
            'source': bn_url.split('/')[2],
            'date': date
        }
        
        out_path = self.output_dir / f"{pair_id}.json"
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    def _align_paragraphs(self, bn_text: str, en_text: str) -> List[Tuple[str, str]]:
        """Align Bengali and English paragraphs"""
        # Split into sentences
        bn_sents = self._split_sentences(bn_text)
        en_sents = self._split_sentences(en_text)
        
        # Simple length-based alignment
        aligned = []
        bn_idx = en_idx = 0
        
        while bn_idx < len(bn_sents) and en_idx < len(en_sents):
            bn_sent = self._clean_text(bn_sents[bn_idx])
            en_sent = self._clean_text(en_sents[en_idx])
            
            # Skip empty sentences
            if not bn_sent:
                bn_idx += 1
                continue
            if not en_sent:
                en_idx += 1
                continue
            
            # Check length ratio is reasonable
            ratio = len(bn_sent) / len(en_sent) if len(en_sent) > 0 else 0
            if 0.5 <= ratio <= 2.5:
                aligned.append((bn_sent, en_sent))
                bn_idx += 1
                en_idx += 1
            else:
                # Skip likely misaligned sentence
                if len(bn_sent) < len(en_sent):
                    bn_idx += 1
                else:
                    en_idx += 1
                    
        return aligned
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean text by removing extra whitespace and normalizing"""
        import re
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but preserve Bengali Unicode
        text = re.sub(r'[^\u0980-\u09FF\s\w\.\?\!\,\'\"\(\)\-]', '', text)
        
        return text.strip()
    
    @staticmethod 
    def _split_sentences(text: str) -> List[str]:
        """Split text into sentences"""
        import re
        # Split on । (Bengali full stop), . ! ?
        sentences = re.split(r'[।\.\!\?]', text)
        return [s.strip() for s in sentences if s.strip()]
