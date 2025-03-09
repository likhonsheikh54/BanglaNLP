---
description: Quick start guide for using BanglaNLP for Bengali-English dataset creation
title: Quick Start - BanglaNLP
tags:
  - quick start
  - tutorial
  - getting started
---

# Quick Start Guide

This guide will help you quickly get started with BanglaNLP to create a Bengali-English parallel corpus from news sources.

## Prerequisites

Before beginning, ensure you have:

- Installed BanglaNLP (see [Installation Guide](installation.md))
- A stable internet connection for web scraping

## Basic Usage

### 1. Running the Basic Scraper

The simplest way to start is to run the default scraper with the following command:

```bash
python main.py
```

This will:

- Scrape articles from all configured news sources
- Extract and align Bengali-English sentence pairs
- Save the dataset in the `data` directory

### 2. Customizing the Scraper

You can customize the scraping process with command-line arguments:

```bash
python main.py --sources prothomalo ittefaq --max-articles 200 --output custom_data
```

This command will:

- Only scrape from Prothom Alo and Ittefaq sources
- Limit to 200 articles per source
- Save the output to the `custom_data` directory

### 3. Viewing the Dataset

After scraping, you can view the dataset statistics:

```bash
python -c "import pandas as pd; df = pd.read_json('data/dataset.json', lines=True); print(f'Total pairs: {len(df)}'); print(df.source.value_counts())"
```

### 4. Uploading to Hugging Face

Upload your dataset to Hugging Face with:

```bash
python main.py --upload --hf-repo yourusername/bengali-english-news
```

Ensure you have first logged in to Hugging Face using `huggingface-cli login`.

## Example Workflow

Here's a complete workflow for creating and using the dataset:

```bash
# 1. Clone the repository and install dependencies
git clone https://github.com/likhonsheikh54/BanglaNLP.git
cd BanglaNLP
pip install -r requirements.txt

# 2. Run the scraper with customizations
python main.py --sources prothomalo ittefaq banglatribune --max-articles 500

# 3. Check the dataset quality
python scripts/analyze_dataset.py

# 4. Upload to Hugging Face
python main.py --upload --hf-repo yourusername/bengali-english-news

# 5. Use the dataset for machine translation
python scripts/train_mt_model.py
```

## Using the Dataset in Your Code

### Loading with Pandas

```python
import pandas as pd

# Load the dataset
df = pd.read_json('data/dataset.json', lines=True)

# Print some examples
print(df.head())

# Filter by source
prothomalo_pairs = df[df.source == 'prothomalo']
print(f"Prothom Alo pairs: {len(prothomalo_pairs)}")
```

### Loading with Hugging Face Datasets

```python
from datasets import load_dataset

# Load from local files
dataset = load_dataset('json', data_files={
    'train': 'data/train.json',
    'validation': 'data/validation.json',
    'test': 'data/test.json'
})

# Or from Hugging Face Hub
online_dataset = load_dataset('BanglaNLP/bengali-english-news')

# Use for machine translation
print(f"Training examples: {len(dataset['train'])}")
print(f"Example pair: {dataset['train'][0]}")
```

## Scheduled Scraping

For continuous dataset updates, set up a cron job or scheduled task:

```bash
# Create a script to run scraping
echo "#!/bin/bash
cd /path/to/BanglaNLP
python main.py --max-articles 100 --upload" > update_dataset.sh
chmod +x update_dataset.sh

# Add to crontab (runs daily at 2 AM)
crontab -e
# Add this line: 0 2 * * * /path/to/update_dataset.sh
```

## Next Steps

Now that you've created a basic dataset, you can:

- Configure additional news sources (see [Configuration Guide](configuration.md))
- Explore advanced filtering options (see [Filtering Guide](../features/filtering.md))
- Learn about dataset format details (see [Dataset Format](../dataset/format.md))
- Contribute to the project (see [Contributing Guide](../contributing.md))
