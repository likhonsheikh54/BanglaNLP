---
description: Installation guide for BanglaNLP - Bengali-English dataset creation toolkit
title: Installation - BanglaNLP
tags:
  - installation
  - setup
  - requirements
---

# Installation Guide

## Requirements

Before installing BanglaNLP, make sure you have the following prerequisites installed:

- Python 3.7 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Basic Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/likhonsheikh54/BanglaNLP.git
cd BanglaNLP
```

### Step 2: Install Dependencies

Install all required packages using pip:

```bash
pip install -r requirements.txt
```

This will install all the necessary dependencies including:

- beautifulsoup4 - For HTML parsing
- requests - For HTTP requests
- pandas - For data manipulation
- tqdm - For progress bars
- datasets - For HuggingFace dataset compatibility
- langdetect - For language detection
- huggingface_hub - For uploading to HuggingFace

## Development Installation

If you plan to contribute to the development of BanglaNLP, we recommend installing in development mode:

```bash
pip install -e .
```

This creates an editable installation that automatically reflects any changes you make to the source code.

## Environment Setup with Conda

Alternatively, you can use conda to create an isolated environment:

```bash
# Create a new conda environment
conda create -n bangla-nlp python=3.9

# Activate the environment
conda activate bangla-nlp

# Install dependencies
pip install -r requirements.txt
```

## Docker Installation

For containerized deployment, we provide a Dockerfile:

```bash
# Build the Docker image
docker build -t bangla-nlp .

# Run a container with mounted data volume
docker run -v $(pwd)/data:/app/data bangla-nlp
```

## Troubleshooting

### Common Issues

1. **SSL Certificate Errors**

   If you encounter SSL certificate errors when making requests, try installing the certifi package:

   ```bash
   pip install certifi
   ```

2. **Bengali Font Display Issues**

   If Bengali characters don't display correctly, ensure your terminal or editor supports UTF-8:

   ```python
   # Check Python's default encoding
   import sys
   print(sys.getdefaultencoding())
   # Should output 'utf-8'
   ```

3. **Memory Errors During Large Dataset Processing**

   For large datasets, you may need to process data in batches:

   ```bash
   python main.py --max-articles 100  # Process in smaller batches
   ```

## Verification

To verify your installation, run the test script:

```bash
python -m unittest discover tests
```

You should see all tests pass without errors.

## Next Steps

After installation, check out the [Quick Start Guide](quickstart.md) to begin using BanglaNLP.
