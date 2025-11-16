#!/usr/bin/env python3
"""Test du scraper RSS"""

from scrapers.rss_scraper import RSScraper

# Sites à tester
sites = [
    'https://www.sidwaya.info',
    'https://www.aib.media',
    'https://burkina24.com',
    'https://lefaso.net',
]

print("🧪 Test du scraper RSS\n")
print("="*60)

for site in sites:
    print(f"\n📡 Test: {site}")
    print("-"*60)
    
    scraper = RSScraper(site)
    
    # Trouver le flux RSS
    rss_url = scraper.find_rss_feed()
    
    if rss_url:
        print(f"✅ Flux RSS: {rss_url}")
        
        # Récupérer les articles
        articles = scraper.get_articles_from_rss(days=30, max_articles=5)
        
        if articles:
            print(f"✅ {len(articles)} articles trouvés\n")
            print("📰 Premiers articles:")
            for i, article in enumerate(articles[:3], 1):
                print(f"\n   {i}. {article['titre'][:60]}...")
                print(f"      URL: {article['url'][:70]}...")
                print(f"      Date: {article['date_publication']}")
                if article.get('auteur'):
                    print(f"      Auteur: {article['auteur']}")
        else:
            print("❌ Aucun article trouvé")
    else:
        print("❌ Pas de flux RSS")
    
    print()

print("\n" + "="*60)
print("✅ Test terminé")
