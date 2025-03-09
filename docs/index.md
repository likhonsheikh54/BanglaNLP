---
description: BanglaNLP - A comprehensive toolkit for creating high-quality Bengali-English parallel datasets from news sources
title: BanglaNLP - Bengali-English Machine Translation Dataset Creation Tools
tags:
  - bengali
  - english
  - machine translation
  - dataset
  - nlp
---

# BanglaNLP: Bengali-English Dataset Toolkit

[![GitHub stars](https://img.shields.io/github/stars/likhonsheikh54/BanglaNLP?style=social)](https://github.com/likhonsheikh54/BanglaNLP)
[![Telegram](https://img.shields.io/badge/Join-RecentCoders-blue?logo=telegram)](https://t.me/RecentCoders)

Welcome to **BanglaNLP** - a comprehensive toolkit for creating high-quality Bengali-English parallel datasets from news sources.

<div class="grid cards" markdown>

-   :material-code-json:

    ---

    **Dataset Creation**

    Automated scraping and alignment of Bengali-English news articles

-   :material-filter-outline:

    ---

    **Quality Filtering**

    Advanced filtering mechanisms to ensure high-quality translation pairs

-   :material-database:

    ---

    **Hugging Face Integration**

    Seamless integration with the Hugging Face ecosystem

-   :material-robot:

    ---

    **Automation**

    Schedule and automate dataset creation and updates

</div>

## Overview

BanglaNLP is a project that addresses the challenge of building high-quality Bengali-English parallel corpora for machine translation. Despite Bengali being spoken by over 230 million people worldwide, it remains a relatively low-resource language in NLP research.

This toolkit provides:

* Scrapers for major Bengali news websites
* Sentence alignment algorithms
* Quality filtering mechanisms
* Dataset formatting for machine learning
* Hugging Face integration

## Key Features

- **Multi-source Scraping**: Extract content from 6 major Bengali news sources
- **Intelligent Alignment**: Automatically align Bengali-English sentence pairs
- **Quality Filtering**: Remove noisy or misaligned translations
- **Extensible Architecture**: Easily add new news sources
- **Hugging Face Integration**: Direct upload to Hugging Face Hub
- **Comprehensive Documentation**: Detailed guides and API reference

## Quick Installation

```bash
git clone https://github.com/likhonsheikh54/BanglaNLP.git
cd BanglaNLP
pip install -r requirements.txt
```

## Basic Usage

```bash
# Run with default settings
python main.py

# Specify sources and limit articles
python main.py --sources prothomalo ittefaq --max-articles 500

# Upload to Hugging Face
python main.py --upload --hf-repo yourusername/bengali-english-news
```

## Sample Dataset Entry

```json
{
  "bn": "বাংলাদেশ জলবায়ু পরিবর্তনের প্রভাবে সবচেয়ে বেশি ক্ষতিগ্রস্ত দেশগুলির মধ্যে একটি।",
  "en": "Bangladesh is one of the countries most affected by climate change.",
  "source": "prothomalo",
  "url": "https://www.prothomalo.com/environment/climate-change-impacts"
}
```

## Project Status

The project is under active development. Current version supports:

- 6 major Bengali news sources
- Parallel text extraction and alignment
- Dataset quality filtering
- Hugging Face integration

## Resources

- [GitHub Repository](https://github.com/likhonsheikh54/BanglaNLP)
- [Dataset on Hugging Face](https://huggingface.co/datasets/BanglaNLP/bengali-english-news)
- [RecentCoders Telegram Channel](https://t.me/RecentCoders)

## Community & Support

Join our community on [Telegram](https://t.me/RecentCoders) for discussions about Bengali NLP, machine translation, and related topics.

---

<small>Powered by [RecentCoders](https://t.me/RecentCoders) - A hub for developers, innovators, and tech enthusiasts shaping the future of coding.</small>
