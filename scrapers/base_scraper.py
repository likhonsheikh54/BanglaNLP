import requests
from bs4 import BeautifulSoup
from .config import USER_AGENT
import logging

class BaseScraper:
    def __init__(self, source_config):
        self.base_url = source_config['base_url']
        self.article_selector = source_config['article_selector']
        self.headers = {'User-Agent': USER_AGENT}
        
    def get_page(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            return None

    def extract_article(self, url):
        """
        Extract article content from URL
        Returns: dict with title, content, date, etc.
        """
        soup = self.get_page(url)
        if not soup:
            return None
            
        # Implement article extraction logic
        return {
            'url': url,
            'title': '',
            'content': '',
            'date': '',
            'language': ''
        }
    
    def discover_article_urls(self, list_url):
        """Get article URLs from a listing page"""
        soup = self.get_page(f"{self.base_url}{list_url}")
        if not soup:
            return []
            
        links = soup.select(self.source_config['link_selector'])
        urls = []
        for link in links:
            href = link.get('href')
            if href:
                if not href.startswith('http'):
                    href = f"{self.base_url}{href}"
                urls.append(href)
        return urls
