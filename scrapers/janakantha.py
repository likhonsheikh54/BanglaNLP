import logging
from .base_scraper import BaseScraper

class JanakanthaScraper(BaseScraper):
    def extract_article(self, url):
        soup = self.get_page(url)
        if not soup:
            return None
            
        try:
            title = soup.select_one('h1.news-title').text.strip()
            content = ' '.join([p.text.strip() for p in soup.select('div.news-content p')])
            date = soup.select_one('span.date').text.strip()
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
