#!/usr/bin/env python3
"""Debug du scraper HTML"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url = "https://lepays.bf"

print(f"🔍 Test HTML scraping: {url}\n")

# Récupérer la page
response = requests.get(url, timeout=30)
soup = BeautifulSoup(response.content, 'lxml')

print(f"✅ Page récupérée: {len(response.content)} bytes\n")

# Tester différents sélecteurs
selectors = [
    'article a[href]',
    '.post a[href]',
    '.entry a[href]',
    'h2 a[href]',
    'h3 a[href]',
    '.entry-title a[href]',
    'a[href*="/20"]',  # URLs avec année
]

print("📋 Test des sélecteurs:\n")

for selector in selectors:
    elements = soup.select(selector)
    print(f"   {selector}: {len(elements)} éléments")
    
    if len(elements) > 0 and len(elements) <= 5:
        for elem in elements[:3]:
            href = elem.get('href')
            if href:
                full_url = urljoin(url, href)
                print(f"      → {full_url}")

print("\n" + "="*60)
print("🔍 Recherche de tous les liens internes:\n")

all_links = soup.find_all('a', href=True)
internal_links = []

for link in all_links:
    href = link.get('href')
    full_url = urljoin(url, href)
    
    # Vérifier que c'est un lien interne
    if urlparse(full_url).netloc == urlparse(url).netloc:
        # Exclure les patterns non-articles
        excluded = ['/category/', '/tag/', '/author/', '/page/', 
                   '/wp-admin/', '/wp-content/', '.jpg', '.png', 
                   '/contact', '/about']
        
        is_excluded = any(pattern in full_url.lower() for pattern in excluded)
        
        if not is_excluded and full_url not in internal_links:
            internal_links.append(full_url)

print(f"Total liens internes (filtrés): {len(internal_links)}")
print("\n📰 Premiers 10 liens d'articles potentiels:\n")

for i, link in enumerate(internal_links[:10], 1):
    print(f"   {i}. {link}")

print("\n" + "="*60)
