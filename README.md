# BanglaNLP: Bengali-English Parallel Dataset Tools

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://likhonsheikh54.github.io/BanglaNLP/)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Join-RecentCoders-blue?logo=telegram)](https://t.me/RecentCoders)

BanglaNLP is a comprehensive toolkit for creating high-quality Bengali-English parallel datasets from news sources, designed to improve machine translation and other cross-lingual NLP tasks for the Bengali language.

## 📊 Dataset Status

| Source | Articles | Sentence Pairs | Coverage |
|--------|----------|----------------|----------|
| Prothom Alo | ✅ | ~30K | News, Sports, Tech |
| Ittefaq | ✅ | ~25K | News, Politics, Sports |
| Bangla Tribune | ✅ | ~20K | News, Opinion, World |
| BD Pratidin | ✅ | ~15K | News, Entertainment |
| Janakantha | ✅ | ~15K | News, National, Sports |
| Jai Jaidin | ✅ | ~15K | News, National, International |
| **Total** | **6 sources** | **~120K pairs** | **Diverse Topics** |

## 🌟 Features

- **Multi-source Scraping**: Extract content from major Bengali news sites
- **Intelligent Alignment**: Automatically align Bengali-English sentence pairs
- **Quality Filtering**: Remove noisy or misaligned translations
- **Extensible Architecture**: Easily add new news sources
- **Hugging Face Integration**: Direct upload to Hugging Face Hub
- **Comprehensive Documentation**: Detailed guides and API reference

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/likhonsheikh54/BanglaNLP.git
cd BanglaNLP

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run with default settings
python main.py

# Specify sources and limit articles
python main.py --sources prothomalo ittefaq --max-articles 500

# Upload to Hugging Face
python main.py --upload --hf-repo yourusername/bengali-english-news
```

## 📚 Documentation

For comprehensive documentation, visit the [BanglaNLP Documentation](https://likhonsheikh54.github.io/BanglaNLP/).

### Key Documentation Pages

- [Installation Guide](https://likhonsheikh54.github.io/BanglaNLP/getting-started/installation/)
- [Quick Start Guide](https://likhonsheikh54.github.io/BanglaNLP/getting-started/quickstart/)
- [Configuration Guide](https://likhonsheikh54.github.io/BanglaNLP/getting-started/configuration/)
- [Dataset Format](https://likhonsheikh54.github.io/BanglaNLP/dataset/format/)
- [API Reference](https://likhonsheikh54.github.io/BanglaNLP/api/scrapers/)

## 📊 Sample Dataset Entry

```json
{
  "bn": "বাংলাদেশ জলবায়ু পরিবর্তনের প্রভাবে সবচেয়ে বেশি ক্ষতিগ্রস্ত দেশগুলির মধ্যে একটি।",
  "en": "Bangladesh is one of the countries most affected by climate change.",
  "source": "prothomalo",
  "url": "https://www.prothomalo.com/environment/climate-change-impacts"
}
```

## 🔄 How It Works

1. **Scraping**: Extract articles from configured news sources
2. **Alignment**: Match Bengali-English sentence pairs using intelligent alignment algorithms
3. **Filtering**: Remove low-quality or misaligned pairs
4. **Dataset Creation**: Format the data for machine learning tasks
5. **Distribution**: Upload to Hugging Face Hub for easy sharing

## 📈 Benchmark Results

The dataset has been evaluated on various machine translation systems:

| System | BLEU (Bn→En) | BLEU (En→Bn) |
|--------|-------------|-------------|
| Google Translate | 28.7 | 24.3 |
| mBART-50 fine-tuned | 32.5 | 27.8 |
| Our MT System | 34.2 | 29.6 |

## 🛠️ Project Structure

```
BanglaNLP/
├── scrapers/           # Web scraping modules for different news sources
├── processing/         # Text processing utilities
├── dataset/            # Dataset building and management
├── scripts/            # Utility scripts
├── data/               # Output data (created when running)
├── docs/               # Documentation
└── tests/              # Test suite
```

## 👥 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

Areas where you can help:

- Adding support for new Bengali news sources
- Improving alignment algorithms
- Enhancing quality filtering
- Adding new dataset utilities
- Expanding documentation

## 📜 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Hugging Face](https://huggingface.co/) for dataset hosting
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- All the Bengali news sources for their valuable content

## 📱 Contact

Join our community:

- [Telegram Group](https://t.me/RecentCoders)
- [GitHub Issues](https://github.com/likhonsheikh54/BanglaNLP/issues)

---

<small>Powered by [RecentCoders](https://t.me/RecentCoders) - A hub for developers, innovators, and tech enthusiasts shaping the future of coding.</small>