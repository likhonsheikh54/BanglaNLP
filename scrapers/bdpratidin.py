import logging
from .base_scraper import BaseScraper

class BDPratidinScraper(BaseScraper):
    def extract_article(self, url):
        soup = self.get_page(url)
        if not soup:
            return None
            
        try:
            title = soup.select_one('h2.news-title').text.strip()
            content = ' '.join([p.text.strip() for p in soup.select('div.news-details p')])
            date = soup.select_one('span.time').text.strip()
            language = 'bn' if '/bangla/' in url else 'en'
            
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
