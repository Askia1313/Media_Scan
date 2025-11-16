#!/usr/bin/env python3
"""Test du scraper HTML intelligent"""

from scrapers.smart_html_scraper import SmartHTMLScraper
from bs4 import BeautifulSoup

url = "https://lepays.bf"

print(f"🔍 Test du scraper intelligent: {url}\n")

scraper = SmartHTMLScraper(url)

# Récupérer la page
soup = scraper.get_page(url)

if not soup:
    print("❌ Impossible de récupérer la page")
    exit(1)

print(f"✅ Page récupérée\n")

# Tester les sélecteurs
selectors = [
    'article.post a[href]',
    'article a.entry-title[href]',
    '.post-item a[href]',
    '.entry-title a[href]',
    'article h2 a[href]',
    'h2 a[href]',
    'h3 a[href]',
    'a[href*="/202"]',
]

print("📋 Test des sélecteurs:\n")

for selector in selectors:
    elements = soup.select(selector)
    print(f"   {selector}: {len(elements)} éléments")
    if len(elements) > 0 and len(elements) <= 3:
        for elem in elements[:2]:
            href = elem.get('href')
            if href:
                from urllib.parse import urljoin
                full_url = urljoin(url, href)
                is_article = scraper._is_article_url(full_url)
                print(f"      → {full_url[:80]}... [Article: {is_article}]")

print("\n" + "="*60)
print("🔍 Recherche élargie de tous les liens:\n")

all_links = soup.find_all('a', href=True)
print(f"Total liens trouvés: {len(all_links)}")

article_links = []
for link in all_links[:50]:  # Tester les 50 premiers
    href = link.get('href')
    from urllib.parse import urljoin, urlparse
    full_url = urljoin(url, href)
    
    # Vérifier que c'est un lien interne
    if urlparse(full_url).netloc == urlparse(url).netloc:
        if scraper._is_article_url(full_url):
            article_links.append(full_url)

print(f"\nLiens d'articles trouvés: {len(article_links)}")
print("\n📰 Premiers 10 liens d'articles:\n")

for i, link in enumerate(article_links[:10], 1):
    print(f"   {i}. {link}")
