from .base_scraper import BaseScraper
import logging

class BDPratidinScraper(BaseScraper):
    def extract_article(self, url):
        soup = self.get_page(url)
        if not soup:
            return None
            
        try:
            title = soup.select_one('h1.detail-title').text.strip()
            content = ' '.join([p.text.strip() for p in soup.select('div.news-details p')])
            date = soup.select_one('span.details-time').get_text(strip=True)
            language = 'bn'  # BD Pratidin is primarily Bengali
            
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
