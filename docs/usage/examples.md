---
description: Examples and code snippets demonstrating common usage patterns for BanglaNLP
title: Examples - BanglaNLP
tags:
  - examples
  - code snippets
  - tutorials
---

# Examples

This page provides practical examples and code snippets for common usage patterns with BanglaNLP.

## Basic Examples

### Scraping a Single News Source

```python
from scrapers.prothomalo import ProthomAloScraper
from scrapers.config import NEWS_SOURCES

# Initialize the scraper
scraper = ProthomAloScraper(NEWS_SOURCES['prothomalo'])

# Scrape articles
articles = scraper.scrape(max_articles=10)

# Print the titles
for article in articles:
    print(f"Title: {article['title']}")
    print(f"URL: {article['url']}")
    print("-" * 50)
```

### Building a Dataset from Scraped Content

```python
from dataset.dataset_builder import DatasetBuilder

# Initialize the dataset builder
dataset = DatasetBuilder()

# Load scraped data
dataset.load_from_directory("data/raw")

# Process and filter the data
dataset.process()

# Create train/validation/test splits
dataset.create_splits(test_size=0.1, val_size=0.1)

# Save the dataset
dataset.save("data/processed")

# Print dataset statistics
stats = dataset.generate_statistics()
print(f"Total pairs: {stats['total_pairs']}")
print(f"Train set: {stats['by_split']['train']} pairs")
print(f"Validation set: {stats['by_split']['validation']} pairs")
print(f"Test set: {stats['by_split']['test']} pairs")
```

### Uploading to Hugging Face

```python
from huggingface_hub import login
from dataset.dataset_builder import DatasetBuilder

# Login to Hugging Face
login()

# Load dataset
dataset = DatasetBuilder(data_dir="data/processed")

# Upload to Hugging Face
dataset.upload_to_hub(
    repo_id="yourusername/bengali-english-news",
    private=False
)
```

## Advanced Examples

### Custom Text Processing Pipeline

```python
from processing.text_processor import TextProcessor
from processing.segmenter import Segmenter
from dataset.dataset_builder import DatasetBuilder

# Create custom text processor
text_processor = TextProcessor(
    normalize_unicode=True,
    remove_urls=True,
    normalize_numbers=True,
    custom_rules=[
        (r'\[.*?\]', ''),  # Remove content in square brackets
        (r'\(.*?\)', ''),  # Remove content in parentheses
    ]
)

# Create custom segmenter
segmenter = Segmenter(
    min_sentence_length=10,
    respect_paragraphs=True,
    join_short_sentences=True
)

# Initialize dataset builder with custom processors
dataset = DatasetBuilder(
    text_processor=text_processor,
    segmenter=segmenter
)

# Process data with custom pipeline
dataset.load_from_directory("data/raw")
dataset.process()
dataset.save("data/custom_processed")
```

### Creating a Specialized Dataset Subset

```python
import pandas as pd

# Load the full dataset
df = pd.read_json("data/processed/train.json", lines=True)

# Create a subset with specific topics
topics = ['politics', 'sports', 'technology']
topics_subset = df[df['source'].isin(topics)]

# Balance the subset
dataset_size = min(df['source'].value_counts())
balanced_subset = pd.concat([
    df[df['source'] == topic].sample(dataset_size) 
    for topic in topics
])

# Save the specialized subset
balanced_subset.to_json("data/specialized/train.json", orient="records", lines=True)
```

### Using the Dataset for Machine Translation

```python
from datasets import load_dataset
from transformers import MBartForConditionalGeneration, MBartTokenizer

# Load dataset from Hugging Face
dataset = load_dataset("yourusername/bengali-english-news")

# Initialize model and tokenizer
model_name = "facebook/mbart-large-50"
tokenizer = MBartTokenizer.from_pretrained(model_name)
tokenizer.src_lang = "bn_IN"
tokenizer.tgt_lang = "en_XX"
model = MBartForConditionalGeneration.from_pretrained(model_name)

# Prepare a sample for translation
bengali_text = dataset["train"][0]["bn"]
inputs = tokenizer(bengali_text, return_tensors="pt")

# Generate translation
translated_tokens = model.generate(
    **inputs,
    decoder_start_token_id=tokenizer.lang_code_to_id["en_XX"],
    max_length=100
)

# Decode the translation
translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
print(f"Bengali: {bengali_text}")
print(f"Translation: {translation}")
```

## Practical Use Cases

### Analyzing Dataset Quality

```python
import pandas as pd
import matplotlib.pyplot as plt
from langdetect import detect
from collections import Counter

# Load the dataset
df = pd.read_json("data/processed/train.json", lines=True)

# Calculate length statistics
df['bn_length'] = df['bn'].apply(len)
df['en_length'] = df['en'].apply(len)
df['length_ratio'] = df['bn_length'] / df['en_length']

# Plot length distributions
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(df['bn_length'], bins=50, alpha=0.7, label='Bengali')
plt.hist(df['en_length'], bins=50, alpha=0.7, label='English')
plt.legend()
plt.title('Sentence Length Distribution')
plt.xlabel('Length (characters)')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
plt.hist(df['length_ratio'], bins=50)
plt.title('Length Ratio Distribution (Bengali/English)')
plt.xlabel('Ratio')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('data/analysis/length_distributions.png')

# Verify language using random samples
sample_size = min(1000, len(df))
sample = df.sample(sample_size)

language_stats = {"correct": 0, "incorrect": 0}

for _, row in sample.iterrows():
    try:
        bn_detected = detect(row['bn'])
        en_detected = detect(row['en'])
        
        if bn_detected == 'bn' and en_detected == 'en':
            language_stats["correct"] += 1
        else:
            language_stats["incorrect"] += 1
    except:
        language_stats["incorrect"] += 1

print(f"Language detection results on {sample_size} samples:")
print(f"Correct: {language_stats['correct']} ({language_stats['correct']/sample_size*100:.2f}%)")
print(f"Incorrect: {language_stats['incorrect']} ({language_stats['incorrect']/sample_size*100:.2f}%)")
```

### Building a Baseline Translation Model

```python
import numpy as np
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import MBartForConditionalGeneration, MBartTokenizer
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments

# Load dataset
df = pd.read_json("data/processed/train.json", lines=True)

# Create training and evaluation sets
train_df, eval_df = train_test_split(df, test_size=0.1)

# Convert to Hugging Face datasets
train_dataset = Dataset.from_pandas(train_df)
eval_dataset = Dataset.from_pandas(eval_df)

# Initialize tokenizer
model_name = "facebook/mbart-large-50"
tokenizer = MBartTokenizer.from_pretrained(model_name)
tokenizer.src_lang = "bn_IN"
tokenizer.tgt_lang = "en_XX"

# Tokenization function
def tokenize_function(examples):
    bn_texts = examples["bn"]
    en_texts = examples["en"]
    
    model_inputs = tokenizer(bn_texts, max_length=128, truncation=True, padding="max_length")
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(en_texts, max_length=128, truncation=True, padding="max_length")
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Tokenize datasets
train_tokenized = train_dataset.map(tokenize_function, batched=True)
eval_tokenized = eval_dataset.map(tokenize_function, batched=True)

# Initialize model
model = MBartForConditionalGeneration.from_pretrained(model_name)

# Training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=3,
    predict_with_generate=True,
    fp16=True,
)

# Initialize trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_tokenized,
    eval_dataset=eval_tokenized,
    tokenizer=tokenizer,
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained("models/bengali-english-translator")
tokenizer.save_pretrained("models/bengali-english-translator")
```

### Web Service for Translation

```python
from flask import Flask, request, jsonify
from transformers import MBartForConditionalGeneration, MBartTokenizer

app = Flask(__name__)

# Load model and tokenizer
model_path = "models/bengali-english-translator"
tokenizer = MBartTokenizer.from_pretrained(model_path)
model = MBartForConditionalGeneration.from_pretrained(model_path)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text', '')
    source_lang = data.get('source_lang', 'bn_IN')
    target_lang = data.get('target_lang', 'en_XX')
    
    # Set source language
    tokenizer.src_lang = source_lang
    
    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt")
    
    # Generate translation
    translated_tokens = model.generate(
        **inputs,
        decoder_start_token_id=tokenizer.lang_code_to_id[target_lang],
        max_length=256
    )
    
    # Decode translation
    translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    
    return jsonify({
        'source_text': text,
        'translation': translation,
        'source_lang': source_lang,
        'target_lang': target_lang
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Script Examples

### Incremental Dataset Update Script

```python
#!/usr/bin/env python
# scripts/update_dataset.py

import os
import json
import argparse
from datetime import datetime
from dataset.dataset_builder import DatasetBuilder

def main():
    parser = argparse.ArgumentParser(description="Update dataset with new data")
    parser.add_argument("--existing", default="data/processed", help="Path to existing dataset")
    parser.add_argument("--new-data", default="data/raw_new", help="Path to new data")
    parser.add_argument("--output", default="data/updated", help="Output path for updated dataset")
    parser.add_argument("--upload", action="store_true", help="Upload to Hugging Face")
    parser.add_argument("--hf-repo", default=None, help="Hugging Face repository ID")
    args = parser.parse_args()
    
    # Load existing dataset
    existing_dataset = DatasetBuilder(data_dir=args.existing)
    
    # Process new data
    new_dataset = DatasetBuilder()
    new_dataset.load_from_directory(args.new_data)
    new_dataset.process()
    
    # Merge datasets
    existing_dataset.merge(new_dataset, deduplicate=True)
    
    # Create updated splits
    existing_dataset.create_splits(test_size=0.1, val_size=0.1)
    
    # Save updated dataset
    existing_dataset.save(args.output)
    
    # Generate and save statistics
    stats = existing_dataset.generate_statistics()
    with open(os.path.join(args.output, "stats.json"), "w") as f:
        json.dump(stats, f, indent=2)
    
    print(f"Dataset updated: {stats['total_pairs']} total pairs")
    
    # Upload if requested
    if args.upload and args.hf_repo:
        existing_dataset.upload_to_hub(args.hf_repo)
        print(f"Dataset uploaded to {args.hf_repo}")

if __name__ == "__main__":
    main()
```

### Dataset Evaluation Script

```python
#!/usr/bin/env python
# scripts/evaluate_dataset.py

import argparse
import pandas as pd
import numpy as np
from sacrebleu import sentence_bleu
from transformers import pipeline

def main():
    parser = argparse.ArgumentParser(description="Evaluate dataset quality using translation models")
    parser.add_argument("--test-data", default="data/processed/test.json", help="Test data path")
    parser.add_argument("--model", default="Helsinki-NLP/opus-mt-bn-en", help="Translation model to use")
    parser.add_argument("--output", default="data/evaluation_results.json", help="Output file for results")
    args = parser.parse_args()
    
    # Load test data
    df = pd.read_json(args.test_data, lines=True)
    
    # Sample for evaluation (limit to 1000 examples for time efficiency)
    sample_size = min(1000, len(df))
    sample = df.sample(sample_size)
    
    # Initialize translation pipeline
    translator = pipeline("translation", model=args.model)
    
    # Evaluate samples
    results = []
    for i, row in enumerate(sample.iterrows()):
        i, row = row
        bn_text = row['bn']
        reference = row['en']
        
        # Translate Bengali to English
        translation = translator(bn_text, max_length=128)[0]['translation_text']
        
        # Calculate BLEU score
        bleu = sentence_bleu(translation, [reference]).score
        
        results.append({
            'bn': bn_text,
            'reference': reference,
            'translation': translation,
            'bleu': bleu
        })
        
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{sample_size} examples")
    
    # Calculate aggregate statistics
    bleu_scores = [r['bleu'] for r in results]
    avg_bleu = np.mean(bleu_scores)
    
    # Save results
    evaluation = {
        'model': args.model,
        'sample_size': sample_size,
        'avg_bleu': float(avg_bleu),
        'examples': results
    }
    
    pd.Series(evaluation).to_json(args.output)
    
    print(f"Evaluation complete. Average BLEU score: {avg_bleu:.2f}")
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()
```

## Next Steps

After exploring these examples, you might want to check out:

- [Command Line Interface](cli.md) for details on the CLI options
- [Automation Guide](automation.md) for setting up automated workflows
- [API Reference](../api/scrapers.md) for detailed documentation of the BanglaNLP API
