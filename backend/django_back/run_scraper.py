#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal pour lancer le scraping des médias
"""

import sys
import argparse
from pathlib import Path

# Ajouter le dossier parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import DatabaseManager
from scrapers.scraper_manager import ScraperManager


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description='MÉDIA-SCAN - Scraper de médias burkinabè'
    )
    
    parser.add_argument(
        '--sites-file',
        type=str,
        default='sites.txt',
        help='Fichier contenant les URLs des sites (défaut: sites.txt)'
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Nombre de jours à récupérer (défaut: 30)'
    )
    
    parser.add_argument(
        '--db-path',
        type=str,
        default='data/media_scan.db',
        help='Chemin vers la base de données (défaut: data/media_scan.db)'
    )
    
    parser.add_argument(
        '--url',
        type=str,
        help='Scraper un seul site (URL)'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Afficher les statistiques de la base de données'
    )
    
    args = parser.parse_args()
    
    # Initialiser la base de données
    print("🔧 Initialisation de la base de données...")
    db = DatabaseManager(db_path=args.db_path)
    
    # Afficher les stats si demandé
    if args.stats:
        print_stats(db)
        return
    
    # Initialiser le gestionnaire de scraping
    manager = ScraperManager(db)
    
    # Scraper un seul site ou tous les sites
    if args.url:
        # Scraper un seul site
        count, method, message = manager.scrape_site(args.url, days=args.days)
        print(f"\n{message}")
    else:
        # Scraper tous les sites du fichier
        stats = manager.scrape_all_sites(
            sites_file=args.sites_file,
            days=args.days
        )
        
        # Afficher les stats finales
        print("\n📊 Statistiques de la base de données:")
        print_stats(db)


def print_stats(db: DatabaseManager):
    """Afficher les statistiques de la base de données"""
    stats = db.get_scraping_stats()
    
    print("\n" + "="*60)
    print("📊 STATISTIQUES DE LA BASE DE DONNÉES")
    print("="*60)
    
    print(f"\n📰 Total articles: {stats['total_articles']}")
    
    print(f"\n📺 Articles par média:")
    for media, count in stats['articles_par_media'].items():
        print(f"   • {media}: {count} articles")
    
    print(f"\n🔧 Articles par source:")
    for source, count in stats['articles_par_source'].items():
        print(f"   • {source}: {count} articles")
    
    if stats['derniers_logs']:
        print(f"\n📋 Derniers logs de scraping:")
        for log in stats['derniers_logs'][:5]:
            status_icon = "✅" if log['status'] == 'success' else "❌"
            print(f"   {status_icon} {log['media_nom']}: {log['articles_collectes']} articles ({log['methode']})")
            if log['message']:
                print(f"      → {log['message']}")
    
    print("\n" + "="*60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interruption par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
