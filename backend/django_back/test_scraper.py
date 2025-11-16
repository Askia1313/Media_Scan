#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier le scraping
"""

import sys
from pathlib import Path

# Ajouter le dossier parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import DatabaseManager
from scrapers.wordpress_scraper import WordPressScraper
from scrapers.html_scraper import HTMLScraper


def test_wordpress_detection():
    """Tester la détection WordPress"""
    print("\n" + "="*60)
    print("TEST 1: Détection WordPress")
    print("="*60)
    
    test_sites = [
        'https://lefaso.net',
        'https://www.sidwaya.info',
        'https://www.fasopresse.net'
    ]
    
    for url in test_sites:
        print(f"\n🔍 Test: {url}")
        scraper = WordPressScraper(url)
        is_wp = scraper.is_wordpress()
        
        if is_wp:
            print(f"   ✅ WordPress détecté")
        else:
            print(f"   ❌ WordPress non détecté")


def test_wordpress_scraping():
    """Tester le scraping WordPress"""
    print("\n" + "="*60)
    print("TEST 2: Scraping WordPress")
    print("="*60)
    
    # Initialiser la base de données
    db = DatabaseManager('data/test_media_scan.db')
    
    # Tester avec Lefaso.net (probablement WordPress)
    url = 'https://lefaso.net'
    print(f"\n📡 Test scraping: {url}")
    
    try:
        scraper = WordPressScraper(url)
        
        if scraper.is_wordpress():
            # Ajouter le média
            media_id = db.add_media('Lefaso.net', url, 'wordpress')
            
            # Scraper (limité à 5 articles pour le test)
            articles = scraper.scrape(media_id, days=30)
            
            print(f"\n✅ {len(articles)} articles récupérés")
            
            # Afficher les 3 premiers
            for i, article in enumerate(articles[:3], 1):
                print(f"\n   Article {i}:")
                print(f"   • Titre: {article.titre[:80]}...")
                print(f"   • URL: {article.url}")
                print(f"   • Date: {article.date_publication}")
                print(f"   • Auteur: {article.auteur}")
                print(f"   • Contenu: {len(article.contenu)} caractères")
            
            # Sauvegarder en base
            saved = 0
            for article in articles:
                if db.add_article(article):
                    saved += 1
            
            print(f"\n💾 {saved} articles sauvegardés en base de données")
        
        else:
            print("❌ Ce site n'utilise pas WordPress")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


def test_html_scraping():
    """Tester le scraping HTML"""
    print("\n" + "="*60)
    print("TEST 3: Scraping HTML")
    print("="*60)
    
    # Initialiser la base de données
    db = DatabaseManager('data/test_media_scan.db')
    
    # Tester avec un site
    url = 'https://www.aib.media'
    print(f"\n🌐 Test scraping HTML: {url}")
    
    try:
        scraper = HTMLScraper(url)
        
        # Ajouter le média
        media_id = db.add_media('AIB', url, 'html')
        
        # Scraper (limité à 5 articles pour le test)
        articles = scraper.scrape(media_id, days=30, max_articles=5)
        
        print(f"\n✅ {len(articles)} articles récupérés")
        
        # Afficher les articles
        for i, article in enumerate(articles, 1):
            print(f"\n   Article {i}:")
            print(f"   • Titre: {article.titre[:80]}...")
            print(f"   • URL: {article.url}")
            print(f"   • Contenu: {len(article.contenu)} caractères")
        
        # Sauvegarder en base
        saved = 0
        for article in articles:
            if db.add_article(article):
                saved += 1
        
        print(f"\n💾 {saved} articles sauvegardés en base de données")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


def test_database():
    """Tester les opérations de base de données"""
    print("\n" + "="*60)
    print("TEST 4: Base de données")
    print("="*60)
    
    db = DatabaseManager('data/test_media_scan.db')
    
    # Statistiques
    stats = db.get_scraping_stats()
    
    print(f"\n📊 Statistiques:")
    print(f"   • Total articles: {stats['total_articles']}")
    print(f"   • Articles par média: {stats['articles_par_media']}")
    print(f"   • Articles par source: {stats['articles_par_source']}")
    
    # Récupérer les articles récents
    recent = db.get_recent_articles(days=30, limit=5)
    
    print(f"\n📰 {len(recent)} articles récents:")
    for article in recent:
        print(f"   • {article.titre[:60]}... ({article.date_publication})")


def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("🧪 TESTS DU SYSTÈME DE SCRAPING")
    print("="*60)
    
    try:
        # Test 1: Détection WordPress
        test_wordpress_detection()
        
        # Test 2: Scraping WordPress
        test_wordpress_scraping()
        
        # Test 3: Scraping HTML
        test_html_scraping()
        
        # Test 4: Base de données
        test_database()
        
        print("\n" + "="*60)
        print("✅ TESTS TERMINÉS")
        print("="*60)
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrompus")
    except Exception as e:
        print(f"\n❌ Erreur globale: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
