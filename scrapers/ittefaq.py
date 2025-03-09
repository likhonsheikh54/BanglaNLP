import logging
from .base_scraper import BaseScraper

class IttefaqScraper(BaseScraper):
    def extract_article(self, url):
        soup = self.get_page(url)
        if not soup:
            return None
            
        try:
            title = soup.select_one('h2.title-news').text.strip()
            content = ' '.join([p.text.strip() for p in soup.select('div.dtl-news-txt p')])
            date = soup.select_one('div.news-time').text.strip()
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
