---
description: Learn about the quality filtering mechanisms in BanglaNLP for creating high-quality Bengali-English parallel datasets
title: Filtering Features - BanglaNLP
tags:
  - filtering
  - quality control
  - data cleaning
---

# Filtering Features

The quality of a machine translation dataset is critical for training effective models. BanglaNLP implements several filtering mechanisms to ensure high-quality sentence pairs while maximizing dataset size.

## Filtering Pipeline

The filtering pipeline consists of multiple layers, each addressing different quality aspects:

<div class="mermaid">
graph TD
    A[Raw Extracted Pairs] --> B[Length Filtering]
    B --> C[Ratio Filtering]
    C --> D[Language Detection]
    D --> E[Content Filtering]
    E --> F[Duplication Removal]
    F --> G[Final Filtered Dataset]
</div>

## Length Filtering

Filters out sentence pairs that are too short or too long, as they may not be useful for training or could be noise.

```python
# Minimum length filtering (in characters)
if len(bn) < 20 or len(en) < 20:
    continue
    
# Maximum length filtering (optional)
if len(bn) > 1000 or len(en) > 1000:
    continue
```

### Customization

You can adjust the length thresholds in `dataset_builder.py` under `_apply_quality_filters` method:

```python
# Adjust these values in dataset_builder.py
MIN_CHARS = 20  # Minimum characters per sentence
MAX_CHARS = 1000  # Maximum characters per sentence

# Or pass as parameters when running
python main.py --min-length 30 --max-length 800
```

## Length Ratio Filtering

Filters out pairs where the length ratio between Bengali and English is outside a reasonable range, indicating potential misalignment.

```python
# Calculate length ratio between Bengali and English
ratio = len(bn) / len(en) if len(en) > 0 else 0

# Check if within acceptable range
if not (0.5 <= ratio <= 3.0):
    continue
```

The default range of 0.5 to 3.0 accounts for the natural length differences between Bengali and English sentences.

## Language Detection

Verifies that the sentences are actually in the expected languages using the `langdetect` library:

```python
from langdetect import detect, LangDetectException

try:
    bn_lang = detect(bn)
    en_lang = detect(en)
    if not (bn_lang == 'bn' and en_lang == 'en'):
        continue
except LangDetectException:
    # Language detection can fail for very short texts
    pass
```

### Confidence Scores

For more stringent filtering, confidence scores can be used:

```python
from langdetect import DetectorFactory
DetectorFactory.seed = 0  # For reproducibility

detector = DetectorFactory.create()
detector.append(text)
langs = detector.get_probabilities()

# Get confidence for the detected language
conf = next((l.prob for l in langs if l.lang == expected_lang), 0)
if conf < 0.8:  # Minimum confidence threshold
    continue
```

## Content Filtering

Filters out pairs based on content quality indicators:

### Special Characters Ratio

```python
def special_char_ratio(text):
    special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
    return special_chars / len(text) if len(text) > 0 else 0

# Too many special characters may indicate parsing issues
if special_char_ratio(bn) > 0.3 or special_char_ratio(en) > 0.3:
    continue
```

### HTML Tag Detection

```python
import re

# Check for HTML tags that might have been improperly scraped
if re.search(r'<[a-z][\s\S]*>', bn) or re.search(r'<[a-z][\s\S]*>', en):
    continue
```

### Numeral Consistency

```python
def extract_numerals(text):
    return re.findall(r'\d+', text)

# Check if numerals are consistent between pairs
bn_nums = extract_numerals(bn)
en_nums = extract_numerals(en)

if len(bn_nums) != len(en_nums) or sorted(bn_nums) != sorted(en_nums):
    continue
```

## Duplication Removal

Removes duplicate or near-duplicate sentence pairs to avoid over-representation:

```python
# Simple exact match deduplication
seen_pairs = set()
for pair in all_pairs:
    key = (pair['bn'], pair['en'])
    if key in seen_pairs:
        continue
    seen_pairs.add(key)
    filtered_pairs.append(pair)
```

### Near-duplicate Detection

For more advanced deduplication, similarity measures can be used:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create TF-IDF vectorizer for each language
bn_vectorizer = TfidfVectorizer()
bn_tfidf = bn_vectorizer.fit_transform([p['bn'] for p in pairs])

en_vectorizer = TfidfVectorizer()
en_tfidf = en_vectorizer.fit_transform([p['en'] for p in pairs])

# Calculate similarity matrices
bn_similarity = cosine_similarity(bn_tfidf)
en_similarity = cosine_similarity(en_tfidf)

# Find pairs with high similarity
duplicates = set()
for i in range(len(pairs)):
    for j in range(i+1, len(pairs)):
        if bn_similarity[i,j] > 0.9 and en_similarity[i,j] > 0.9:
            duplicates.add(j)  # Mark the second occurrence as duplicate

# Filter out duplicates
filtered_pairs = [pairs[i] for i in range(len(pairs)) if i not in duplicates]
```

## Sentence Segmentation Validation

Checks that sentence segmentation is consistent:

```python
def count_sentences(text):
    # Count sentence-ending punctuation
    bn_count = text.count('।')  # Bengali full stop
    en_count = sum(1 for c in text if c in '.!?')
    return max(bn_count, en_count)

# Check if sentence counts are consistent
bn_sentences = count_sentences(bn)
en_sentences = count_sentences(en)

if abs(bn_sentences - en_sentences) > 1:  # Allow small differences
    continue
```

## Filtering Statistics

The filtering process logs statistics to help understand data quality:

```python
from collections import Counter
filtering_stats = Counter()

for pair in pairs:
    bn, en = pair['bn'], pair['en']
    
    if len(bn) < MIN_CHARS or len(en) < MIN_CHARS:
        filtering_stats['short_length'] += 1
        continue
        
    ratio = len(bn) / len(en) if len(en) > 0 else 0
    if not (MIN_RATIO <= ratio <= MAX_RATIO):
        filtering_stats['bad_ratio'] += 1
        continue
    
    # More filters...
    
    filtering_stats['passed'] += 1
    filtered_pairs.append(pair)

# Print statistics
print(f"Filtering statistics:\n{filtering_stats}")
```

## Customizing Filtering

You can customize the filtering pipeline by modifying the `_apply_quality_filters` method in `dataset_builder.py` or by creating a custom filtering class:

```python
class CustomFilterer:
    def __init__(self, min_length=20, max_length=1000, min_ratio=0.5, max_ratio=3.0):
        self.min_length = min_length
        self.max_length = max_length
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio
        self.stats = Counter()
        
    def filter_pairs(self, pairs):
        filtered = []
        for pair in pairs:
            if self.apply_filters(pair):
                filtered.append(pair)
        return filtered, self.stats
        
    def apply_filters(self, pair):
        # Implement your custom filtering logic
        # Return True to keep the pair, False to filter it out
        pass
```

## Custom Filtering Rules

You can create custom filtering rules based on your specific requirements. Examples include:

### Named Entity Consistency

Check that named entities are preserved across languages:

```python
from spacy import load

nlp_bn = load('bn_core_news_sm')  # Bengali SpaCy model
nlp_en = load('en_core_web_sm')   # English SpaCy model

def check_entities(bn_text, en_text):
    bn_doc = nlp_bn(bn_text)
    en_doc = nlp_en(en_text)
    
    bn_ents = set(ent.text.lower() for ent in bn_doc.ents)
    en_ents = set(ent.text.lower() for ent in en_doc.ents)
    
    # Some entities should match (especially proper nouns)
    common_count = len(bn_ents.intersection(en_ents))
    return common_count > 0 if bn_ents and en_ents else True
```

### Sentiment Consistency

Check that the sentiment is preserved across languages:

```python
from textblob import TextBlob
from textblob_bn import BengaliBlob

def check_sentiment(bn_text, en_text):
    bn_sentiment = BengaliBlob(bn_text).sentiment.polarity
    en_sentiment = TextBlob(en_text).sentiment.polarity
    
    # Check if sentiments have same sign (positive/negative)
    return (bn_sentiment * en_sentiment > 0) or abs(bn_sentiment) < 0.2 or abs(en_sentiment) < 0.2
```

## Next Steps

Now that you understand the filtering features, you might want to explore:

- [Dataset Creation](dataset.md) to learn how the filtered pairs are processed
- [Hugging Face Integration](huggingface.md) to understand how to share your dataset
- [API Reference](../api/dataset.md) for detailed implementation details
