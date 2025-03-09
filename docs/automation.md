# Automated Data Collection

## GitHub Actions Workflows

### Scraping Pipeline

The scraping process runs automatically every 6 hours:

1. Scrapes new articles from configured sources
2. Validates sentence pairs
3. Updates HuggingFace dataset
4. Creates GitHub release (on manual trigger)

### Manual Trigger

You can manually trigger the scraping:

1. Go to Actions tab
2. Select "Automated News Scraping"
3. Click "Run workflow"
4. Optionally set max articles per source

## Dataset Validation

The validation script checks:

- Language detection
- Length ratios
- Data format
- Content quality

## HuggingFace Integration

Dataset is automatically published to HuggingFace:

```python
from datasets import load_dataset

dataset = load_dataset("yourusername/bengali-english-news")
```

## Monitoring

- Logs available in Actions tab
- Validation reports in releases
- Dataset statistics in HuggingFace
