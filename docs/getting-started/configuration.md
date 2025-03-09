---
description: Configuration guide for BanglaNLP - Learn how to configure the scraping system for Bengali-English news sources
title: Configuration - BanglaNLP
tags:
  - configuration
  - setup
  - customization
---

# Configuration Guide

This guide explains how to configure BanglaNLP to customize scraping behavior, add new news sources, and modify dataset generation parameters.

## Scraper Configuration

The primary configuration for news sources is in `scrapers/config.py`. This file contains a dictionary of news sources with their base URLs, CSS selectors, and page URLs to scrape.

### News Source Configuration Structure

```python
NEWS_SOURCES = {
    'sourcename': {
        'base_url': 'https://www.example.com',
        'article_selector': 'div.article-class',
        'link_selector': 'h2.title a',
        'list_urls': [
            '/category1',
            '/category2'
        ]
    },
    # More sources...
}
```

### Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|--------|
| `base_url` | Root URL of the news site | `'https://www.prothomalo.com'` |
| `article_selector` | CSS selector for article containers | `'article.story-card'` |
| `link_selector` | CSS selector for article links | `'a.link-overlay'` |
| `list_urls` | List of URL paths to scrape | `['/international', '/sports']` |

### Adding a New News Source

To add a new Bengali news source:

1. Examine the website structure to identify CSS selectors
2. Add a new entry to the `NEWS_SOURCES` dictionary
3. Create a new scraper class that extends `BaseScraper`
4. Register the scraper in `main.py`

Example of adding a new source:

```python
# In scrapers/config.py
NEWS_SOURCES = {
    # Existing sources...
    'newssource': {
        'base_url': 'https://www.newsbangla.com',
        'article_selector': 'div.news-item',
        'link_selector': 'h3.title a',
        'list_urls': [
            '/bangladesh',
            '/international'
        ]
    }
}

# In scrapers/newssource.py
from .base_scraper import BaseScraper
import logging

class NewsSourceScraper(BaseScraper):
    def extract_article(self, url):
        soup = self.get_page(url)
        if not soup:
            return None
            
        try:
            title = soup.select_one('h1.article-title').text.strip()
            content = ' '.join([p.text.strip() for p in soup.select('div.article-content p')])
            date = soup.select_one('span.date').get_text(strip=True)
            language = 'bn'
            
            return {
                'url': url,
                'title': title,
                'content': content, 
                'date': date,
                'language': language
            }
        except Exception as e:
            logging.error(f"Error extracting from {url}: {str(e)}")
            return None

# In main.py, add to scrapers dictionary
scrapers = {
    # Existing scrapers...
    'newssource': NewsSourceScraper
}
```

## Command Line Arguments

The `main.py` script accepts several command line arguments to customize execution:

```bash
python main.py --help
```

Output:

```
usage: main.py [-h] [--output OUTPUT] [--max-articles MAX_ARTICLES]
               [--sources SOURCES [SOURCES ...]] [--upload] [--hf-repo HF_REPO]

Bengali-English News Dataset Builder

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output directory for dataset
  --max-articles MAX_ARTICLES, -m MAX_ARTICLES
                        Maximum number of articles to scrape per source
  --sources SOURCES [SOURCES ...], -s SOURCES [SOURCES ...]
                        News sources to scrape
  --upload, -u          Upload dataset to Hugging Face
  --hf-repo HF_REPO     Hugging Face repository name
```

### Examples

```bash
# Scrape specific sources and limit articles
python main.py --sources prothomalo ittefaq --max-articles 200

# Change output directory
python main.py --output datasets/march2023

# Upload to custom HF repo
python main.py --upload --hf-repo yourusername/bengali-english-custom
```

## Advanced Configuration

### Logging Configuration

Logging is configured in `main.py` using Python's built-in logging module. By default, logs are saved in the `logs` directory with a timestamp in the filename.

You can adjust log levels and handlers in the `setup_logging` function:

```python
def setup_logging(log_dir='logs', log_level=logging.INFO):
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'scraping_{timestamp}.log')
    
    logging.basicConfig(
        level=log_level,  # Change this to adjust verbosity
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
```

### Dataset Quality Filtering

Quality filtering parameters can be adjusted in `dataset/dataset_builder.py` in the `_apply_quality_filters` method:

```python
def _apply_quality_filters(self, pairs: List[Dict]) -> List[Dict]:
    filtered = []
    
    for pair in tqdm(pairs, desc="Filtering"):
        bn, en = pair['bn'], pair['en']
        
        # Adjust minimum length requirement
        if len(bn) < 20 or len(en) < 20:  # Change these values
            continue
            
        # Adjust length ratio bounds
        ratio = len(bn) / len(en) if len(en) > 0 else 0
        if not (0.5 <= ratio <= 3.0):  # Change these values
            continue
            
        # Other filters...
        
        filtered.append(pair)
        
    return filtered
```

### Creating a Configuration File

For more flexible configuration, you can create a JSON or YAML configuration file:

```json
{
  "scraping": {
    "max_articles": 500,
    "timeout": 30,
    "user_agent": "Mozilla/5.0 ..."
  },
  "dataset": {
    "output_dir": "data",
    "min_sentence_length": 20,
    "min_length_ratio": 0.5,
    "max_length_ratio": 3.0
  },
  "huggingface": {
    "repo": "yourusername/bengali-english-news",
    "private": false
  }
}
```

Then update your script to load this configuration:

```python
import json

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)
        
def main():
    args = parse_args()
    config = load_config(args.config)
    # Use config values throughout the script
```

## Environment Variables

You can also use environment variables for sensitive configuration values like API keys:

```python
# In your code
import os

hf_token = os.environ.get('HUGGINGFACE_TOKEN')
```

And set them when running:

```bash
HUGGINGFACE_TOKEN=your_token python main.py --upload
```

Or persistently in your `.bashrc` or `.env` file:

```
# .env file
HUGGINGFACE_TOKEN=your_token
```

```python
# Load .env file
from dotenv import load_dotenv
load_dotenv()
```

## Next Steps

Now that you understand how to configure BanglaNLP, you might want to explore:

- [Scraping Features](../features/scraping.md) for advanced scraping capabilities
- [Dataset Creation](../features/dataset.md) for customizing dataset generation
- [API Reference](../api/scrapers.md) for detailed implementation details
