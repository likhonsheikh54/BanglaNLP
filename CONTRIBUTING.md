# Contributing to BanglaNLP

First off, thank you for considering contributing to BanglaNLP! It's people like you that make BanglaNLP such a great tool for Bengali-English NLP research and applications.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Adding New News Sources](#adding-new-news-sources)
  - [Improving Documentation](#improving-documentation)
  - [Implementing Features](#implementing-features)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
  - [Code Style](#code-style)
  - [Commit Messages](#commit-messages)
- [License](#license)

## Code of Conduct

This project and everyone participating in it is governed by the BanglaNLP Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [telegram@RecentCoders](https://t.me/RecentCoders).

## Getting Started

Follow these steps to set up BanglaNLP for local development:

1. Fork the BanglaNLP repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/BanglaNLP.git
   cd BanglaNLP
   ```
3. Create a branch for local development:
   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Environment

We recommend using a virtual environment for development:

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda
conda create -n bangla-nlp python=3.9
conda activate bangla-nlp
```

Install the development dependencies:

```bash
pip install -e ".[dev]"
```

This will install all required dependencies, plus additional packages for testing and development.

## How Can I Contribute?

### Reporting Bugs

Bugs are tracked as GitHub issues. Before creating bug reports, please check if the issue has already been reported. When creating a bug report, include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Describe the behavior you observed after following the steps
- Explain what behavior you expected to see instead
- Include versions of relevant software (Python, OS, etc.)
- Include screenshots or terminal output if applicable

### Suggesting Enhancements

Enhancement suggestions are also tracked as GitHub issues. When suggesting an enhancement:

- Use a clear and descriptive title
- Provide a detailed description of the suggested enhancement
- Explain why this enhancement would be useful to BanglaNLP users
- Include any relevant examples or references

### Adding New News Sources

One of the most valuable contributions is adding support for new Bengali news sources. To add a new news source:

1. Identify a Bengali news source that provides both Bengali and English content
2. Study the website structure to identify CSS selectors for:
   - Article listings
   - Article content
   - Publication dates
   - Article titles
3. Create a new scraper class in `scrapers/` directory (use existing scrapers as templates)
4. Add configuration for the new source in `scrapers/config.py`
5. Register the scraper in `main.py`
6. Test the scraper thoroughly
7. Update documentation to include the new source

Example for adding a new scraper:

```python
# In scrapers/newsource.py
from .base_scraper import BaseScraper
import logging

class NewSourceScraper(BaseScraper):
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
```

### Improving Documentation

Documentation improvements are always welcome! The documentation is written in Markdown and organized in the `docs/` directory. To update documentation:

1. Edit the relevant Markdown files
2. If adding a new page, update `mkdocs.yml` to include it in the navigation
3. Test your changes by running `mkdocs serve`
4. Submit a pull request with your changes

### Implementing Features

Feature implementation should follow these steps:

1. Discuss the feature in a GitHub issue to get feedback
2. Fork the repository and create a feature branch
3. Implement the feature with appropriate tests
4. Document the feature in the appropriate documentation files
5. Submit a pull request for review

## Pull Request Process

1. Update the README.md or documentation with details of changes, if applicable
2. Add or update tests for any new functionality
3. Make sure all tests pass before submitting the PR
4. Update the CHANGELOG.md with details of your changes
5. The PR will be merged once it receives approval from maintainers

## Style Guidelines

### Code Style

We follow PEP 8 style guidelines for Python code. Key points:

- Use 4 spaces for indentation (not tabs)
- Use docstrings for all public methods and functions
- Maximum line length is 100 characters
- Use snake_case for variable and function names
- Use CamelCase for class names

We use `flake8` for code linting. Run it before submitting a PR:

```bash
flake8 .
```

### Commit Messages

Commit messages should be clear and descriptive. Use the present tense ("Add feature" not "Added feature") and imperative mood ("Move cursor to..." not "Moves cursor to...").

Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types include:
- feat: A new feature
- fix: A bug fix
- docs: Documentation only changes
- style: Changes that do not affect the meaning of the code
- refactor: Code change that neither fixes a bug nor adds a feature
- test: Adding missing tests or correcting existing tests
- chore: Changes to the build process or auxiliary tools

Example:
```
feat(scraper): add support for Daily Star Bangladesh

Implements a new scraper for Daily Star Bangladesh newspaper.
Supports both Bengali and English article extraction.

Resolves: #123
```

## License

By contributing to BanglaNLP, you agree that your contributions will be licensed under the project's [GNU GPL v3 License](LICENSE).

---

Thank you for contributing to BanglaNLP! Your efforts help improve machine translation and NLP research for the Bengali language.
