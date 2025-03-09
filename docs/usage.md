# Usage Guide

## Installation

### Using pip
```bash
pip install git+https://github.com/yourusername/BanglaNLP.git
```

### From source
```bash
git clone https://github.com/yourusername/BanglaNLP.git
cd BanglaNLP
pip install -e .
```

## Running the Scraper

### Command Line
```bash
bangla-scrape
```

### As a Python Package
```python
from bangla_nlp.scraping.coordinator import ScrapingCoordinator

coordinator = ScrapingCoordinator("output_dir")
coordinator.register_scraper("prothomalo", ProthomAloScraper)
coordinator.run(max_articles=1000)
```

## Dataset Format

### File Structure
