---
description: Learn about the structure and organization of BanglaNLP dataset for Bengali-English parallel corpus
title: Dataset Structure - BanglaNLP
tags:
  - dataset
  - structure
  - organization
---

# Dataset Structure

This page explains the structure and organization of datasets created with BanglaNLP. Understanding this structure is important for both using the dataset effectively and contributing to its development.

## Directory Structure

By default, BanglaNLP organizes its datasets with the following directory structure:

```
BanglaNLP/
├── data/
│   ├── raw/                   # Raw scraped articles by source
│   │   ├── prothomalo/
│   │   ├── ittefaq/
│   │   └── ...
│   ├── processed/              # Processed and aligned sentence pairs
│   │   ├── prothomalo.json
│   │   ├── ittefaq.json
│   │   └── ...
│   ├── train.json              # Training split
│   ├── validation.json         # Validation split
│   ├── test.json               # Test split
│   ├── metadata.json           # Dataset metadata
│   └── README.md               # Dataset card for Hugging Face
└── ...
```

## Split Organization

BanglaNLP automatically generates train, validation, and test splits from the processed data. These splits are designed to be automatically detected by Hugging Face's dataset loading utilities.

### Default Split Ratios

By default, the dataset is split with the following proportions:

- **Train**: 80% of the data
- **Validation**: 10% of the data
- **Test**: 10% of the data

You can customize these ratios when building the dataset:

```python
from dataset.dataset_builder import DatasetBuilder

dataset = DatasetBuilder(data_dir="data/processed")
dataset.build_dataset(
    test_size=0.15,    # 15% for test
    val_size=0.15,     # 15% for validation
    output_dir="data"
)
```

### Manual Split Configuration

For more control over which files go into which split, you can create a dataset configuration file:

```yaml
# dataset_config.yaml
configs:
  - config_name: default
    data_files:
      - split: train
        path: prothomalo.json
      - split: train
        path: ittefaq.json
      - split: validation
        path: banglatribune.json
      - split: test
        path: bdpratidin.json
```

Then apply this configuration when building:

```python
dataset.build_dataset_from_config("dataset_config.yaml", output_dir="data")
```

## File Formats

BanglaNLP primarily works with JSON files for maximum flexibility, but supports conversion to other formats for specific use cases.

### JSON Format

The default format is [JSON Lines](https://jsonlines.org/), where each line is a valid JSON object representing a sentence pair:

```json
{"bn": "বাংলাদেশ জলবায়ু পরিবর্তনের প্রভাবে সবচেয়ে বেশি ক্ষতিগ্রস্ত দেশগুলির মধ্যে একটি।", "en": "Bangladesh is one of the countries most affected by climate change.", "source": "prothomalo", "url": "https://www.prothomalo.com/environment/climate-change-impacts"}
{"bn": "আমরা সবাই জানি যে প্লাস্টিক দূষণ একটি বড় সমস্যা।", "en": "We all know that plastic pollution is a major problem.", "source": "ittefaq", "url": "https://www.ittefaq.com.bd/environment/614325"}
```

This format is compatible with Hugging Face's `datasets` library and easy to parse with standard JSON libraries.

### Parquet Format

For large datasets, Parquet provides better compression and faster access:

```python
# Convert to Parquet
dataset.convert_to_parquet(input_dir="data", output_dir="data_parquet")
```

This creates Parquet files with the same structure but better performance:

```
data_parquet/
├── train.parquet
├── validation.parquet
└── test.parquet
```

### CSV Format

For simple use cases or compatibility with spreadsheet software:

```python
# Convert to CSV
dataset.convert_to_csv(input_dir="data", output_dir="data_csv")
```

This creates CSV files with the following columns:

```
bn,en,source,url
"বাংলাদেশ জলবায়ু পরিবর্তনের প্রভাবে সবচেয়ে বেশি ক্ষতিগ্রস্ত দেশগুলির মধ্যে একটি।","Bangladesh is one of the countries most affected by climate change.","prothomalo","https://www.prothomalo.com/environment/climate-change-impacts"
```

## Dataset Subsets

For larger datasets, you might want to create subsets with different characteristics.

### Topic-based Subsets

You can organize data by topic:

```yaml
# topic_config.yaml
configs:
  - config_name: news
    data_files:
      - split: train
        path: data/topics/news_train.json
      - split: test
        path: data/topics/news_test.json
  
  - config_name: sports
    data_files:
      - split: train
        path: data/topics/sports_train.json
      - split: test
        path: data/topics/sports_test.json
```

### Size-based Subsets

Create subsets of different sizes for benchmarking:

```yaml
# size_config.yaml
configs:
  - config_name: full
    data_files:
      - split: train
        path: data/train.json
      - split: validation
        path: data/validation.json
      - split: test
        path: data/test.json
  
  - config_name: small
    data_files:
      - split: train
        path: data/small_train.json
      - split: test
        path: data/small_test.json
```

## Dataset Fields

The core fields in the BanglaNLP dataset are:

| Field | Type | Description |
|-------|------|-------------|
| `bn` | string | Bengali text |
| `en` | string | English translation |
| `source` | string | Source website identifier |
| `url` | string | URL of the original article (when available) |

### Extended Fields

Depending on configuration, additional fields may be present:

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Publication date of the article |
| `title_bn` | string | Bengali article title |
| `title_en` | string | English article title |
| `quality_score` | float | Quality assessment score (0-1) |
| `tags` | list | List of topic tags |

## Metadata

Each dataset includes a metadata.json file with information about its creation:

```json
{
  "created_at": "2023-05-15T10:30:45",
  "version": "1.0.0",
  "sources": ["prothomalo", "ittefaq", "banglatribune"],
  "statistics": {
    "total_pairs": 120000,
    "by_source": {
      "prothomalo": 30000,
      "ittefaq": 25000,
      "banglatribune": 20000
    },
    "by_split": {
      "train": 100000,
      "validation": 10000,
      "test": 10000
    }
  },
  "processing": {
    "filters_applied": ["length", "ratio", "language_detection"],
    "min_length": 20,
    "max_length": 1000,
    "min_ratio": 0.5,
    "max_ratio": 3.0
  }
}
```

This metadata helps track the dataset's provenance and processing steps.

## Dataset Card

The README.md file serves as a dataset card when published to Hugging Face. It includes:

1. **YAML Metadata**: Machine-readable information about the dataset
2. **Overview**: General description and purpose
3. **Structure**: Detailed explanation of fields and organization
4. **Creation**: How the dataset was created
5. **Usage**: Examples of how to use the dataset
6. **Limitations**: Known limitations and biases
7. **Citation**: How to cite the dataset

## Image and Audio Examples

While BanglaNLP focuses on text, it can be extended to include image and audio data. For these modalities, a structured approach is recommended:

### Image Dataset Structure

```
data/
├── images/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── metadata.csv          # Contains image paths and captions in Bengali and English
└── README.md
```

For image datasets, the metadata.csv might look like:

```csv
image_path,bn_caption,en_caption,source
images/image1.jpg,"বাংলাদেশের সুন্দরবন।","The Sundarbans of Bangladesh.","prothomalo"
```

### Audio Dataset Structure

```
data/
├── audio/
│   ├── audio1.mp3
│   ├── audio2.mp3
│   └── ...
├── metadata.csv          # Contains audio paths and transcriptions in Bengali and English
└── README.md
```

For audio datasets, the metadata.csv might look like:

```csv
audio_path,bn_transcription,en_transcription,source
audio/audio1.mp3,"বাংলাদেশ একটি সুন্দর দেশ।","Bangladesh is a beautiful country.","voice_recording"
```

## Next Steps

Now that you understand the dataset structure, you might want to explore:

- [Dataset Format Details](format.md) for in-depth information about the data format
- [Hugging Face Integration](../features/huggingface.md) for publishing your dataset
- [Quality Metrics](../features/filtering.md) for evaluating dataset quality
