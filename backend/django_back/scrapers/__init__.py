"""
Module de scraping multi-sources
"""

from .wordpress_scraper import WordPressScraper
from .html_scraper import HTMLScraper
from .scraper_manager import ScraperManager

__all__ = ['WordPressScraper', 'HTMLScraper', 'ScraperManager']
