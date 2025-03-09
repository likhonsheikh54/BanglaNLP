from .base_scraper import BaseScraper

class ProthomAloScraper(BaseScraper):
    def extract_article(self, url):
        soup = self.get_page(url)
        if not soup:
            return None
            
        try:
            title = soup.select_one('h1.title').text.strip()
            content = ' '.join([p.text.strip() for p in soup.select('div.story-element p')])
            date = soup.select_one('time').get('datetime', '')
            language = 'bn' if soup.html.get('lang', '').startswith('bn') else 'en'
            
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
