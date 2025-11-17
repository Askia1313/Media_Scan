#!/usr/bin/env python3
"""
Script de scraping Facebook depuis la table media
Récupère les posts des pages Facebook configurées dans la table medias
"""

import argparse
import os
from dotenv import load_dotenv
from database.db_manager import DatabaseManager
from scrapers.facebook_scraper import FacebookScraper

# Charger les variables d'environnement
load_dotenv()


def scrape_facebook_for_media(db: DatabaseManager, fb_scraper: FacebookScraper, 
                              media_id: int, media_nom: str, fb_page: str, limit: int = 10):
    """Scraper Facebook pour un média"""
    print(f"\n📘 Scraping Facebook: {media_nom} (@{fb_page})")
    
    try:
        result = fb_scraper.scrape_page(fb_page, limit=limit)
        
        if result.get('error'):
            print(f"   ❌ Erreur: {result['error']}")
            return 0
        
        posts = result.get('posts', [])
        
        if not posts:
            print(f"   ⚠️ Aucun post récupéré")
            return 0
        
        # Sauvegarder les posts
        saved_count = 0
        for post in posts:
            try:
                db.add_facebook_post(
                    media_id=media_id,
                    post_id=post['post_id'],
                    message=post['message'],
                    url=post['url'],
                    image_url=post.get('image_url'),
                    date_publication=post['date_publication'],
                    likes=post['likes'],
                    comments=post['comments'],
                    shares=post['shares']
                )
                saved_count += 1
            except Exception:
                continue
        
        stats = result.get('stats', {})
        print(f"   ✅ {saved_count} posts sauvegardés")
        print(f"   📊 Engagement total: {stats.get('total_engagement', 0):,}")
        
        return saved_count
    
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return 0


def main():
    parser = argparse.ArgumentParser(description='Scraping Facebook depuis table media')
    parser.add_argument('--media-id', type=int, help='ID d\'un média spécifique')
    parser.add_argument('--all', action='store_true', help='Scraper tous les médias avec Facebook')
    parser.add_argument('--limit', type=int, default=10, 
                       help='Nombre de posts à récupérer par média (défaut: 10)')
    
    args = parser.parse_args()
    
    # Vérifier le token Facebook
    fb_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    if not fb_token:
        print("❌ Token Facebook manquant")
        print("💡 Configurez FACEBOOK_ACCESS_TOKEN dans le fichier .env")
        return
    
    # Initialiser
    print("🔧 Initialisation...")
    db = DatabaseManager()
    fb_scraper = FacebookScraper(fb_token)
    
    # Tester la connexion
    if not fb_scraper.test_connection():
        print("❌ Impossible de se connecter à l'API Facebook")
        return
    
    print("✅ Facebook API connectée\n")
    
    # Scraper un média spécifique
    if args.media_id:
        # Récupérer le média
        medias = db.get_all_medias(actif_only=False)
        media = next((m for m in medias if m.id == args.media_id), None)
        
        if not media:
            print(f"❌ Média ID {args.media_id} non trouvé")
            return
        
        if not media.facebook_page:
            print(f"❌ Aucune page Facebook configurée pour {media.nom}")
            return
        
        print("="*60)
        print(f"🎯 Scraping: {media.nom}")
        print("="*60)
        
        scrape_facebook_for_media(
            db, fb_scraper, media.id, media.nom,
            media.facebook_page, args.limit
        )
    
    # Scraper tous les médias avec Facebook
    elif args.all:
        print("="*60)
        print("🚀 SCRAPING FACEBOOK MULTI-MÉDIAS")
        print("="*60)
        
        # Récupérer les médias avec Facebook configuré
        medias = db.get_medias_with_facebook(actif_only=True)
        
        if not medias:
            print("❌ Aucun média avec Facebook configuré")
            print("💡 Ajoutez des pages Facebook dans la table medias")
            return
        
        print(f"\n📋 {len(medias)} médias à scraper\n")
        
        total_posts = 0
        
        for i, media in enumerate(medias, 1):
            print(f"[{i}/{len(medias)}] {media.nom}")
            print("-"*60)
            
            count = scrape_facebook_for_media(
                db, fb_scraper, media.id, media.nom,
                media.facebook_page, args.limit
            )
            
            total_posts += count
        
        # Résumé
        print("\n" + "="*60)
        print("📊 RÉSUMÉ")
        print("="*60)
        print(f"✅ Total posts Facebook: {total_posts}")
        
        # Afficher le top engagement
        print("\n🏆 TOP ENGAGEMENT FACEBOOK (30 derniers jours):")
        ranking = db.get_media_ranking(days=30)
        
        for i, media in enumerate(ranking[:5], 1):
            if media['total_posts_facebook'] > 0:
                print(f"\n{i}. {media['nom']}")
                print(f"   Posts: {media['total_posts_facebook']}")
                print(f"   Likes: {media['total_likes']:,}")
                print(f"   Commentaires: {media['total_comments']:,}")
                print(f"   Partages: {media['total_shares']:,}")
                print(f"   Engagement total: {media['engagement_total']:,}")
    
    else:
        print("❌ Spécifiez --media-id ou --all")
        print("💡 Exemples:")
        print("   python scrape_facebook.py --all")
        print("   python scrape_facebook.py --media-id 1 --limit 20")


if __name__ == '__main__':
    main()
