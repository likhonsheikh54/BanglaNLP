import logging
from .base_scraper import BaseScraper

class JaiJaidinScraper(BaseScraper):
    def extract_article(self, url):
        soup = self.get_page(url)
        if not soup:
            return None
            
        try:
            title = soup.select_one('h2.article-title').text.strip()
            content = ' '.join([p.text.strip() for p in soup.select('div.article-text p')])
            date = soup.select_one('div.publish-date').text.strip()
            language = 'bn' if not '/en/' in url else 'en'
            
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
