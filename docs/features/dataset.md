---
description: Learn about the dataset creation process in BanglaNLP for Bengali-English parallel data
title: Dataset Creation - BanglaNLP
tags:
  - dataset
  - creation
  - processing
---

# Dataset Creation

This page explains the dataset creation process in BanglaNLP, from raw scraped data to a structured, high-quality parallel corpus suitable for machine translation and other NLP tasks.

## Dataset Creation Pipeline

The dataset creation process follows these steps:

<div class="mermaid">
flowchart TD
    A[Web Scraping] --> B[Text Extraction]
    B --> C[Sentence Segmentation]
    C --> D[Sentence Alignment]
    D --> E[Quality Filtering]
    E --> F[Dataset Formatting]
    F --> G[Split Creation]
    G --> H[Dataset Publication]
</div>

## 1. Web Scraping

The process begins with scraping articles from configured Bengali news sources. This is handled by the source-specific scrapers:

```python
from main import run_scrapers

# Run all configured scrapers
run_scrapers(max_articles=1000, output_dir="data/raw")

# Run specific scrapers
run_scrapers(sources=["prothomalo", "ittefaq"], max_articles=500)
```

The scrapers extract article content, titles, publication dates, and other metadata from each news source.

## 2. Text Extraction

Raw HTML content is processed to extract clean text:

```python
from processing.text_processor import clean_text

clean_content = clean_text(raw_content)
```

The text processor performs:

- HTML tag removal
- Special character normalization
- Unicode normalization
- Whitespace standardization
- Removal of irrelevant content (ads, navigation elements, etc.)

## 3. Sentence Segmentation

Extracted text is split into sentences using language-specific segmentation rules:

```python
from processing.segmenter import segment_sentences

bn_sentences = segment_sentences(bn_text, lang="bn")
en_sentences = segment_sentences(en_text, lang="en")
```

The segmenter handles:

- Bengali-specific punctuation (।)
- English punctuation (., !, ?)
- Handling of abbreviations, acronyms, and quotes
- Special cases like bullet points and numbering

## 4. Sentence Alignment

Sentences from parallel articles are aligned to create translation pairs:

```python
from processing.aligner import align_sentences

aligned_pairs = align_sentences(bn_sentences, en_sentences)
```

The aligner uses several techniques:

- Length-based alignment: Matches sentences with similar normalized lengths
- Position-based alignment: Considers relative position in the document
- Content-based alignment: Uses bilingual dictionaries or neural embeddings to match content
- Hybrid approaches: Combines multiple signals for better accuracy

### Alignment Methods

BanglaNLP supports multiple alignment methods that can be configured:

```python
# Length-based alignment
aligned_pairs = align_sentences(bn_sentences, en_sentences, method="length")

# Neural embedding alignment
aligned_pairs = align_sentences(bn_sentences, en_sentences, method="neural")

# Ensemble alignment (combines multiple methods)
aligned_pairs = align_sentences(bn_sentences, en_sentences, method="ensemble")
```

## 5. Quality Filtering

Aligned sentence pairs undergo quality filtering to remove noise:

```python
from dataset.dataset_builder import DatasetBuilder

dataset = DatasetBuilder()
dataset.load_pairs(aligned_pairs)
filtered_pairs = dataset.apply_quality_filters()
```

The filtering process checks for:

- Minimum and maximum sentence lengths
- Appropriate length ratios between Bengali and English
- Language detection to ensure correct languages
- Content heuristics to detect formatting issues
- Duplicate detection and removal

See the [Filtering Features](filtering.md) page for detailed information.

## 6. Dataset Formatting

Filtered pairs are formatted into a structured dataset with consistent fields:

```python
formatted_dataset = dataset.format_dataset()
```

The formatter creates records with the following fields:

- `bn`: Bengali text
- `en`: English translation
- `source`: Source website identifier
- `url`: Original article URL (when available)
- Additional metadata (optional): date, topic, etc.

## 7. Split Creation

The dataset is divided into train, validation, and test splits:

```python
dataset.create_splits(test_size=0.1, val_size=0.1, random_state=42)
```

The split creation process ensures:

- Balanced representation of sources across splits
- Random sampling for statistical validity
- Optional stratification by source or other attributes
- Deterministic behavior with fixed random seed

## 8. Dataset Publication

Finally, the dataset is prepared for sharing:

```python
# Generate dataset card
dataset.create_dataset_card(output_path="data/README.md")

# Upload to Hugging Face (optional)
dataset.upload_to_hub(repo_id="yourusername/bengali-english-news")
```

See the [Hugging Face Integration](huggingface.md) guide for detailed information.

## Using the Dataset Builder

The entire process can be orchestrated using the DatasetBuilder class:

```python
from dataset.dataset_builder import DatasetBuilder

# Initialize the builder
dataset = DatasetBuilder()

# Load scraped data from a directory
dataset.load_from_directory("data/raw")

# Process the data
dataset.process()

# Apply quality filters
dataset.apply_filters()

# Create splits
dataset.create_splits(test_size=0.1, val_size=0.1)

# Save to disk
dataset.save("data/processed")

# Generate statistics
stats = dataset.generate_statistics()
print(stats)
```

## Customizing the Dataset Creation

You can customize the dataset creation process:

### Custom Text Processing

```python
from processing.text_processor import TextProcessor

# Create a custom text processor
processor = TextProcessor(
    normalize_unicode=True,
    remove_urls=True,
    normalize_numbers=False,  # Keep numbers as they are
    custom_rules=[
        (r'\(([^)]+)\)', ''),  # Remove text in parentheses
    ]
)

# Use in dataset builder
dataset = DatasetBuilder(text_processor=processor)
```

### Custom Sentence Alignment

```python
from processing.aligner import Aligner

# Create a custom aligner
aligner = Aligner(
    method="ensemble",
    length_ratio_weight=0.5,
    position_weight=0.3,
    content_weight=0.2,
    max_alignment_size=3  # Allow up to 3 sentences to align to 1
)

# Use in dataset builder
dataset = DatasetBuilder(aligner=aligner)
```

### Custom Quality Filters

```python
# Configure quality filters
dataset = DatasetBuilder()
dataset.configure_filters(
    min_length=30,        # Minimum sentence length
    max_length=500,       # Maximum sentence length
    min_ratio=0.7,        # Minimum length ratio
    max_ratio=2.5,        # Maximum length ratio
    check_language=True,  # Perform language detection
    detect_html=True,     # Check for HTML remnants
    remove_duplicates=True  # Remove duplicate pairs
)
```

## Dataset Versioning

BanglaNLP supports dataset versioning to track changes:

```python
# Create a new version
dataset = DatasetBuilder()
dataset.load_from_directory("data/raw")
dataset.process()
dataset.save("data/processed", version="1.1.0")

# Compare with previous version
diff = dataset.compare_versions("1.0.0", "1.1.0")
print(f"Added: {diff['added']} pairs")
print(f"Removed: {diff['removed']} pairs")
print(f"Modified: {diff['modified']} pairs")
```

## Dataset Statistics

BanglaNLP automatically generates statistics about the dataset:

```python
# Generate and save statistics
stats = dataset.generate_statistics()
dataset.save_statistics("data/stats.json")

# Print summary statistics
print(f"Total pairs: {stats['total_pairs']}")
print(f"By source: {stats['by_source']}")
print(f"Average sentence length (BN): {stats['avg_length_bn']}")
print(f"Average sentence length (EN): {stats['avg_length_en']}")
```

The statistics include:

- Total sentence pairs
- Pairs by source website
- Pairs by split (train/val/test)
- Sentence length distributions
- Type/token ratios
- Vocabulary statistics
- Topic distributions (if available)

## Incremental Dataset Building

For ongoing dataset creation, BanglaNLP supports incremental building:

```python
# Initialize with existing dataset
dataset = DatasetBuilder(existing_dataset_path="data/processed")

# Add new data
dataset.load_from_directory("data/raw_new")
dataset.process()

# Merge with existing data
dataset.merge(deduplicate=True)

# Save updated dataset
dataset.save("data/processed_updated")
```

## Next Steps

Now that you understand the dataset creation process, you might want to explore:

- [Filtering Features](filtering.md) for more details on quality control
- [Dataset Structure](../dataset/structure.md) for information on dataset organization
- [Hugging Face Integration](huggingface.md) for publishing your dataset
