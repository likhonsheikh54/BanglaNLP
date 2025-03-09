import logging
from pathlib import Path
from typing import Dict, Type
from ..scrapers.config import NEWS_SOURCES
from ..scrapers.base_scraper import BaseScraper
from ..dataset.dataset_builder import DatasetBuilder

class ScrapingCoordinator:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.dataset = DatasetBuilder(str(self.output_dir / 'pairs'))
        self.scrapers: Dict[str, Type[BaseScraper]] = {}
        
    def register_scraper(self, name: str, scraper_class: Type[BaseScraper]):
        """Register a scraper for a news source"""
        self.scrapers[name] = scraper_class(NEWS_SOURCES[name])
        
    def run(self, max_articles: int = 1000):
        """Run scraping for all registered sources"""
        for name, scraper in self.scrapers.items():
            logging.info(f"Scraping {name}")
            articles_found = 0
            
            for list_url in NEWS_SOURCES[name]['list_urls']:
                article_urls = scraper.discover_article_urls(list_url)
                
                for url in article_urls:
                    if articles_found >= max_articles:
                        break
                        
                    article = scraper.extract_article(url)
                    if article:
                        # Try to get English version by URL pattern
                        en_url = url.replace('/bn/', '/en/')
                        en_article = scraper.extract_article(en_url)
                        
                        if en_article:
                            self.dataset.add_article_pair(article, en_article)
                            articles_found += 1
                            
            logging.info(f"Found {articles_found} article pairs from {name}")
