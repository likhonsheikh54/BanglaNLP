import logging
from pathlib import Path
import os
import argparse
from datetime import datetime
from scraping.coordinator import ScrapingCoordinator
from scrapers.prothomalo import ProthomAloScraper
from scrapers.ittefaq import IttefaqScraper
from scrapers.banglatribune import BanglaTribuneScraper
from scrapers.bdpratidin import BDPratidinScraper
from scrapers.janakantha import JanakanthaScraper
from scrapers.jaijaidin import JaiJaidinScraper

def setup_logging(log_dir='logs'):
    """Setup logging with rotation"""
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'scraping_{timestamp}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def parse_args():
    parser = argparse.ArgumentParser(description='Bengali-English News Dataset Builder')
    parser.add_argument('--output', '-o', default='data', help='Output directory for dataset')
    parser.add_argument('--max-articles', '-m', type=int, default=1000, 
                        help='Maximum number of articles to scrape per source')
    parser.add_argument('--sources', '-s', nargs='+',
                        default=['prothomalo', 'ittefaq', 'banglatribune', 'bdpratidin', 'janakantha', 'jaijaidin'],
                        help='News sources to scrape')
    parser.add_argument('--upload', '-u', action='store_true', 
                        help='Upload dataset to Hugging Face')
    parser.add_argument('--hf-repo', default='BanglaNLP/bengali-english-news',
                        help='Hugging Face repository name')
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging()
    
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    coordinator = ScrapingCoordinator(str(output_dir))
    
    # Dictionary mapping source names to scraper classes
    scrapers = {
        'prothomalo': ProthomAloScraper,
        'ittefaq': IttefaqScraper,
        'banglatribune': BanglaTribuneScraper,
        'bdpratidin': BDPratidinScraper,
        'janakantha': JanakanthaScraper,
        'jaijaidin': JaiJaidinScraper
    }
    
    # Register only requested scrapers
    for source in args.sources:
        if source in scrapers:
            logging.info(f"Registering scraper for {source}")
            coordinator.register_scraper(source, scrapers[source])
        else:
            logging.warning(f"Unknown source: {source}")
    
    # Run scraping
    coordinator.run(max_articles=args.max_articles)
    
    # Build final dataset
    dataset_path = coordinator.dataset.build_huggingface_dataset()
    logging.info(f"Dataset built at {dataset_path}")
    
    # Upload to Hugging Face if requested
    if args.upload:
        logging.info(f"Uploading dataset to Hugging Face: {args.hf_repo}")
        coordinator.dataset.upload_to_huggingface(args.hf_repo)

if __name__ == '__main__':
    main()
