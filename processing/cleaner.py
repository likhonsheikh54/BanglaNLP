import re
from typing import List, Tuple

class TextCleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep Bengali Unicode
        text = re.sub(r'[^\u0980-\u09FF\s\w\.\?\!]', '', text)
        
        return text.strip()
    
    @staticmethod 
    def split_sentences(text: str) -> List[str]:
        # Split on ।, . ! ?
        sentences = re.split(r'[।\.\!\?]', text)
        return [s.strip() for s in sentences if s.strip()]
        
    @staticmethod
    def align_paragraphs(bn_text: str, en_text: str) -> List[Tuple[str, str]]:
        """
        Align Bengali and English paragraphs using length ratios
        Returns: List of (bengali, english) sentence pairs
        """
        bn_sents = TextCleaner.split_sentences(bn_text)
        en_sents = TextCleaner.split_sentences(en_text)
        
        # Simple length-based alignment
        aligned = []
        bn_idx = en_idx = 0
        
        while bn_idx < len(bn_sents) and en_idx < len(en_sents):
            bn_sent = TextCleaner.clean_text(bn_sents[bn_idx])
            en_sent = TextCleaner.clean_text(en_sents[en_idx])
            
            # Check length ratio is reasonable
            if 0.5 <= len(bn_sent)/len(en_sent) <= 2.0:
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
