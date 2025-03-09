---
description: Guide to using the command-line interface for BanglaNLP - Bengali-English dataset creation toolkit
title: Command Line Interface - BanglaNLP
tags:
  - cli
  - command line
  - usage
---

# Command Line Interface

BanglaNLP provides a comprehensive command-line interface (CLI) for performing all key operations, from scraping to dataset creation and publication.

## Basic Usage

The primary CLI is provided through the `main.py` script:

```bash
python main.py [OPTIONS]
```

## Available Commands

### Scraping Articles

```bash
# Scrape all configured sources with default settings
python main.py

# Scrape specific sources
python main.py --sources prothomalo ittefaq

# Limit the number of articles per source
python main.py --max-articles 200

# Specify output directory
python main.py --output data/custom_scrape

# Combine options
python main.py --sources prothomalo banglatribune --max-articles 500 --output data/march2023
```

### Dataset Building

```bash
# Build dataset from scraped data
python main.py --build

# Customize split sizes
python main.py --build --test-size 0.2 --val-size 0.1

# Apply specific quality filters
python main.py --build --min-length 30 --max-length 500

# Process only specific sources
python main.py --build --include-sources prothomalo ittefaq
```

### Hugging Face Integration

```bash
# Upload dataset to Hugging Face
python main.py --upload --hf-repo yourusername/bengali-english-news

# Build and upload in one command
python main.py --build --upload --hf-repo yourusername/bengali-english-news

# Make the repository private
python main.py --upload --hf-repo yourusername/bengali-english-news --private
```

## Full Command Line Reference

```
usage: main.py [-h] [--sources SOURCES [SOURCES ...]] [--max-articles MAX_ARTICLES]
               [--output OUTPUT] [--build] [--test-size TEST_SIZE]
               [--val-size VAL_SIZE] [--min-length MIN_LENGTH]
               [--max-length MAX_LENGTH] [--include-sources INCLUDE_SOURCES [INCLUDE_SOURCES ...]]
               [--exclude-sources EXCLUDE_SOURCES [EXCLUDE_SOURCES ...]]
               [--upload] [--hf-repo HF_REPO] [--private] [--gated]
               [--debug] [--version]

Bengali-English News Dataset Builder

optional arguments:
  -h, --help            Show this help message and exit
  --sources SOURCES [SOURCES ...], -s SOURCES [SOURCES ...]
                        News sources to scrape
  --max-articles MAX_ARTICLES, -m MAX_ARTICLES
                        Maximum number of articles to scrape per source
  --output OUTPUT, -o OUTPUT
                        Output directory for dataset
  --build, -b           Build dataset from scraped data
  --test-size TEST_SIZE
                        Fraction of data to use for test set
  --val-size VAL_SIZE   Fraction of data to use for validation set
  --min-length MIN_LENGTH
                        Minimum sentence length in characters
  --max-length MAX_LENGTH
                        Maximum sentence length in characters
  --include-sources INCLUDE_SOURCES [INCLUDE_SOURCES ...]
                        Only include these sources in the dataset
  --exclude-sources EXCLUDE_SOURCES [EXCLUDE_SOURCES ...]
                        Exclude these sources from the dataset
  --upload, -u          Upload dataset to Hugging Face
  --hf-repo HF_REPO     Hugging Face repository name
  --private             Make the Hugging Face repository private
  --gated               Enable gated access for the Hugging Face repository
  --debug               Enable debug logging
  --version             Show program version
```

## Specialized Commands

Beyond the main script, BanglaNLP provides specialized scripts for specific tasks:

### Dataset Analysis

```bash
python scripts/analyze_dataset.py --input data/processed
```

This generates statistics and quality metrics for the dataset.

### Dataset Conversion

```bash
# Convert to Parquet format
python scripts/convert_format.py --input data/processed --output data/parquet --format parquet

# Convert to CSV format
python scripts/convert_format.py --input data/processed --output data/csv --format csv
```

### Incremental Updates

```bash
# Perform incremental scraping
python scripts/incremental_update.py --last-run-file last_run.json
```

This script only scrapes new articles since the last run.

## Environment Variables

BanglaNLP CLI also respects environment variables for configuration:

| Variable | Description | Example |
|----------|-------------|--------|
| `BANGLA_NLP_OUTPUT_DIR` | Default output directory | `/path/to/data` |
| `BANGLA_NLP_MAX_ARTICLES` | Default max articles | `500` |
| `HUGGINGFACE_TOKEN` | Hugging Face API token | `hf_...` |
| `BANGLA_NLP_LOG_LEVEL` | Logging level | `DEBUG` |

You can set these in your shell:

```bash
# Set environment variables
export BANGLA_NLP_OUTPUT_DIR="/custom/data/path"
export HUGGINGFACE_TOKEN="your_token_here"

# Then run without specifying these options
python main.py --upload --hf-repo yourusername/bengali-english-news
```

## Config File

For complex configurations, you can use a JSON or YAML config file:

```bash
python main.py --config config.json
```

Example `config.json`:

```json
{
  "sources": ["prothomalo", "ittefaq"],
  "max_articles": 500,
  "output": "data/custom",
  "build": true,
  "test_size": 0.15,
  "val_size": 0.15,
  "min_length": 25,
  "upload": true,
  "hf_repo": "yourusername/bengali-english-news"
}
```

## Shell Completion

To enable shell completion for BanglaNLP CLI commands:

```bash
# For Bash
python -m banglanlp.cli.completion bash > ~/.banglanlp-completion.bash
echo 'source ~/.banglanlp-completion.bash' >> ~/.bashrc

# For Zsh
python -m banglanlp.cli.completion zsh > ~/.banglanlp-completion.zsh
echo 'source ~/.banglanlp-completion.zsh' >> ~/.zshrc
```

## Advanced Usage Examples

### Full Pipeline

Run the complete pipeline from scraping to Hugging Face upload:

```bash
python main.py \
  --sources prothomalo ittefaq banglatribune \
  --max-articles 1000 \
  --output data/march2023 \
  --build \
  --test-size 0.1 \
  --val-size 0.1 \
  --min-length 20 \
  --upload \
  --hf-repo yourusername/bengali-english-news
```

### Filtering Existing Dataset

Apply additional filtering to an existing dataset:

```bash
python scripts/filter_dataset.py \
  --input data/processed \
  --output data/filtered \
  --min-length 30 \
  --max-length 300 \
  --min-ratio 0.5 \
  --max-ratio 2.5
```

### Creating Dataset Subset

Create a smaller subset for experimentation:

```bash
python scripts/create_subset.py \
  --input data/processed \
  --output data/small \
  --size 10000 \
  --stratify source
```

## Troubleshooting

If you encounter issues with the CLI:

1. Enable debug logging: `python main.py --debug`
2. Check log files in the `logs/` directory
3. Verify environment variables with `env | grep BANGLA_NLP`
4. Try running individual components separately (e.g., just scraping first)

## Next Steps

Now that you're familiar with the CLI, you might want to explore:

- [Automation Guide](automation.md) for scheduling and automated workflows
- [API Reference](../api/scrapers.md) for programmatic access
- [Example Scripts](examples.md) for common usage patterns
