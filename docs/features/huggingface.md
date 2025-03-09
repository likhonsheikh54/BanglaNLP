---
description: Guide to publishing your Bengali-English dataset to Hugging Face Hub using BanglaNLP
title: Hugging Face Integration - BanglaNLP
tags:
  - huggingface
  - dataset publishing
  - sharing
---

# Hugging Face Integration

This guide explains how to publish your Bengali-English parallel dataset created with BanglaNLP to the [Hugging Face Hub](https://huggingface.co/datasets), making it accessible to the global NLP community.

## Dataset Structure

Before publishing, it's important to organize your dataset with the proper structure. BanglaNLP provides utilities to format your dataset according to Hugging Face best practices.

### Automatic Split Creation

BanglaNLP can automatically create train, validation, and test splits from your scraped data:

```python
from dataset.dataset_builder import DatasetBuilder

dataset = DatasetBuilder(data_dir="data/scraped")
dataset.build_dataset(test_size=0.1, val_size=0.1)
```

This will create the following structure:

```
data/
├── train.json
├── validation.json
└── test.json
```

Hugging Face will automatically detect these splits based on their filenames.

## Preparing Your Dataset Card

A good dataset card is crucial for users to understand your dataset. BanglaNLP can generate a template dataset card for you:

```python
# Generate a dataset README.md
dataset.create_dataset_card(
    output_path="data/README.md",
    dataset_name="Bengali-English News Corpus",
    author="Your Name",
    email="your.email@example.com"
)
```

The generated README.md includes the required YAML metadata section:

```markdown
---
language: 
  - bn
  - en
pretty_name: "Bengali-English News Corpus"
tags:
  - translation
  - bengali
  - parallel-corpus
  - news
license: "cc-by-4.0"
task_categories:
  - translation
size_categories:
  - 10K<n<100K
features:
  - text
---

# Bengali-English News Corpus

[Detailed description follows...]
```

## Publishing to Hugging Face

BanglaNLP provides built-in functionality to upload your dataset to the Hugging Face Hub:

### Authentication

First, authenticate with Hugging Face:

```bash
# Using the CLI
huggingface-cli login

# Or programmatically in Python
from huggingface_hub import login
login()
```

### Upload from Command Line

```bash
python main.py --upload --hf-repo yourusername/bengali-english-news
```

### Upload Programmatically

```python
from dataset.dataset_builder import DatasetBuilder

dataset = DatasetBuilder(data_dir="data/scraped")

# Build and upload in one step
dataset.build_and_upload(
    test_size=0.1,
    val_size=0.1,
    hf_repo="yourusername/bengali-english-news",
    private=False
)
```

## Dataset Configuration

### Using a Dataset Configuration File

For more complex datasets with multiple subsets or custom configurations, create a `dataset_info.yaml` file:

```yaml
configs:
  - config_name: default
    data_files:
      - split: train
        path: train.json
      - split: validation
        path: validation.json
      - split: test
        path: test.json
        
  - config_name: small
    data_files:
      - split: train
        path: small_train.json
      - split: test
        path: small_test.json
```

Then upload this file alongside your dataset:

```python
dataset.upload_to_hub(
    repo_id="yourusername/bengali-english-news",
    config_path="data/dataset_info.yaml"
)
```

### Supported File Formats

BanglaNLP primarily works with JSON for its flexibility, but you can convert to other formats for specific use cases:

```python
# Convert to Parquet (recommended for large datasets)
dataset.convert_to_parquet()

# Convert to CSV
dataset.convert_to_csv()

# Convert to Arrow streaming format
dataset.convert_to_arrow()
```

## Dataset Card Best Practices

Enhance your dataset card with the following sections:

### Dataset Summary

```markdown
## Dataset Summary

This Bengali-English parallel corpus contains {total_pairs} sentence pairs collected from {num_sources} major Bengali news sources. The dataset is designed for training machine translation systems between Bengali and English.
```

### Supported Tasks

```markdown
## Supported Tasks

- **Machine Translation**: The dataset provides paired Bengali-English sentences for training MT systems.
- **Cross-lingual text generation**: The dataset can be used for training models to generate text across languages.
```

### Dataset Structure

```markdown
## Dataset Structure

### Data Fields

- `bn`: The Bengali text
- `en`: The English translation
- `source`: The source website the pair was extracted from
- `url`: The URL of the original article (when available)
```

### Data Splits

```markdown
## Data Splits

The dataset is divided into train (80%), validation (10%), and test (10%) splits:

| Split | Number of Examples |
|-------|-------------------|
| Train | 100,000 |
| Validation | 10,000 |
| Test | 10,000 |
```

## Access Control

### Private Datasets

You can create a private dataset that requires access approval:

```python
dataset.upload_to_hub(
    repo_id="yourusername/bengali-english-news",
    private=True
)
```

### Gated Datasets

For datasets that require a license agreement or additional information from users:

1. Add the gating information to your README.md:

```markdown
---
extra_gated_prompt: "You agree to use this dataset for research purposes only and to cite the paper in any resulting publications."
extra_gated_fields:
  Institution: text
  Country: country
  Research Purpose:
    type: select
    options: 
      - Academic Research
      - Commercial Research
      - Education
      - Personal Project
  I agree to cite the dataset paper in any resulting publications: checkbox
---
```

2. Upload with gating enabled:

```python
dataset.upload_to_hub(
    repo_id="yourusername/bengali-english-news",
    private=True,
    gated=True
)
```

## Downloading Your Dataset

Once published, users can download your dataset using the Hugging Face `datasets` library:

```python
from datasets import load_dataset

# Load from Hugging Face Hub
dataset = load_dataset("yourusername/bengali-english-news")

# Print some examples
print(dataset["train"][0])
```

## Data Viewer Configuration

To optimize how users can browse your dataset in the Hugging Face Data Viewer, create a `.viewer` file:

```json
{
  "viewer": {
    "table": {
      "columns": [
        "bn",
        "en",
        "source"
      ],
      "filters": [
        "source"
      ]
    }
  }
}
```

This configuration will display the Bengali and English text columns, along with the source, and allow filtering by source.

## Advanced: Hugging Face Hub API

For more advanced use cases, you can use the Hugging Face Hub API directly:

```python
from huggingface_hub import HfApi

api = HfApi()

# Create a new dataset repository
api.create_repo(
    repo_id="yourusername/bengali-english-news",
    repo_type="dataset",
    private=True
)

# Upload files to repository
api.upload_file(
    path_or_fileobj="data/train.json",
    path_in_repo="train.json",
    repo_id="yourusername/bengali-english-news",
    repo_type="dataset"
)
```

## Dataset Citation

Encourage proper citation of your dataset by adding a citation section to your README.md:

```markdown
## Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{sheikh2023bangla,
  author = {Sheikh, Likhon and Contributors},
  title = {Bengali-English News Corpus},
  year = {2023},
  url = {https://huggingface.co/datasets/yourusername/bengali-english-news}
}
```
```

## Next Steps

Now that you've published your dataset, you might want to explore:

- [Creating a Model Card](../api/model_cards.md) for models trained on your dataset
- [Tracking Dataset Usage](../api/metrics.md) to see how your dataset is being used
- [Dataset Versioning](../api/versioning.md) for managing updates to your dataset
