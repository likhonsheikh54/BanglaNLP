---
description: Detailed information about the BanglaNLP dataset format, structure, and specifications
title: Dataset Format - BanglaNLP
tags:
  - dataset
  - format
  - json
  - huggingface
---

# Dataset Format

## Overview

The BanglaNLP dataset is a parallel corpus of Bengali-English sentence pairs extracted from news websites. The dataset is designed for machine translation and other cross-lingual NLP tasks.

## File Structure

The dataset is available in multiple formats:

1. **Raw JSON files**: Individual article pairs stored in the `data/pairs/` directory
2. **JSON Lines format**: Combined dataset in `data/dataset.json` 
3. **Split datasets**: Train/validation/test splits in respective JSON files
4. **Hugging Face format**: Dataset uploaded to the Hugging Face Hub

### Raw JSON Files

Each article pair is stored as a separate JSON file with the following structure:

```json
{
  "id": "a1b2c3d4e5f6g7h8i9j0",
  "bn_url": "https://www.prothomalo.com/bangladesh/article123",
  "en_url": "https://www.prothomalo.com/en/bangladesh/article123",
  "pairs": [
    ["বাংলা বাক্য ১", "English sentence 1"],
    ["বাংলা বাক্য ২", "English sentence 2"],
    // More sentence pairs
  ],
  "source": "prothomalo",
  "date": "2023-03-15T12:30:45Z"
}
```

### JSON Lines Format

The combined dataset in JSON Lines format contains one sentence pair per line:

```json
{"bn": "বাংলা বাক্য ১", "en": "English sentence 1", "source": "prothomalo", "url": "https://www.prothomalo.com/article1", "date": "2023-03-15"}
{"bn": "বাংলা বাক্য ২", "en": "English sentence 2", "source": "ittefaq", "url": "https://www.ittefaq.com/article2", "date": "2023-03-16"}
// More sentence pairs
```

### Split Datasets

The dataset is split into train/validation/test sets with an 80/10/10 ratio:

- `train.json`: 80% of the data, used for training models
- `validation.json`: 10% of the data, used for validation during training
- `test.json`: 10% of the data, used for final evaluation

All split files follow the same JSON Lines format as the full dataset.

## Dataset Fields

| Field | Type | Description |
|-------|------|-------------|
| `bn` | string | Bengali text (source or target) |
| `en` | string | English text (source or target) |
| `source` | string | Name of the news source (e.g., "prothomalo", "ittefaq") |
| `url` | string | URL of the original article |
| `date` | string | Publication date of the article |

## Quality Metrics

The dataset undergoes several quality filtering steps:

1. **Minimum length filtering**: Sentences shorter than 20 characters are removed
2. **Length ratio filtering**: Sentence pairs with bn/en length ratio outside [0.5, 3.0] are removed
3. **Language detection**: Sentences that fail Bengali/English language detection are removed
4. **Duplicate removal**: Duplicate sentence pairs are eliminated

## Loading the Dataset

### Using Python

```python
import pandas as pd

# Load JSON Lines file
df = pd.read_json('data/dataset.json', lines=True)

# Access the data
for index, row in df.iterrows():
    print(f"Bengali: {row['bn']}")
    print(f"English: {row['en']}")
    print(f"Source: {row['source']}")
    print("---")
```

### Using Hugging Face Datasets

```python
from datasets import load_dataset

# Load from local files
dataset = load_dataset('json', data_files={
    'train': 'data/train.json',
    'validation': 'data/validation.json',
    'test': 'data/test.json'
})

# Or load from Hugging Face Hub
dataset = load_dataset('BanglaNLP/bengali-english-news')

# Access the data
for item in dataset['train']:
    print(f"Bengali: {item['bn']}")
    print(f"English: {item['en']}")
    print("---")
```

## Dataset Statistics

The current version of the dataset includes:

- 6 news sources
- ~100,000 sentence pairs (after filtering)
- Average sentence length: ~15 words (Bengali), ~12 words (English)
- Domain coverage: news, politics, sports, technology, entertainment

## Version History

| Version | Date | Description |
|---------|------|-------------|
| v1.0.0 | 2023-03-20 | Initial release with 3 news sources |
| v1.1.0 | 2023-04-15 | Added 3 more news sources and improved quality filtering |
| v1.2.0 | 2023-05-10 | Enhanced dataset with date information and metadata |

## License

The dataset is released under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.
