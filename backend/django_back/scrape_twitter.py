#!/usr/bin/env python3
"""
Script de scraping Twitter depuis la table media
Récupère les tweets des comptes Twitter configurés dans la table medias
"""

import argparse
import os
from dotenv import load_dotenv
from database.db_manager import DatabaseManager
from scrapers.twitter_scraper import TwitterScraper

# Charger les variables d'environnement
load_dotenv()


def scrape_twitter_for_media(db: DatabaseManager, tw_scraper: TwitterScraper,
                             media_id: int, media_nom: str, tw_account: str, limit: int = 10):
    """Scraper Twitter pour un média"""
    print(f"\n🐦 Scraping Twitter: {media_nom} (@{tw_account})")
    
    try:
        result = tw_scraper.scrape_user(tw_account, max_results=limit)
        
        if result.get('error'):
            print(f"   ❌ Erreur: {result['error']}")
            return 0
        
        tweets = result.get('tweets', [])
        
        if not tweets:
            print(f"   ⚠️ Aucun tweet récupéré")
            return 0
        
        # Sauvegarder les tweets
        saved_count = 0
        for tweet in tweets:
            try:
                db.add_twitter_tweet(
                    media_id=media_id,
                    tweet_id=tweet['tweet_id'],
                    text=tweet['text'],
                    url=tweet['url'],
                    image_url=tweet.get('image_url'),
                    date_publication=tweet['date_publication'],
                    retweets=tweet['retweets'],
                    replies=tweet['replies'],
                    likes=tweet['likes'],
                    quotes=tweet['quotes'],
                    impressions=tweet['impressions']
                )
                saved_count += 1
            except Exception:
                continue
        
        stats = result.get('stats', {})
        print(f"   ✅ {saved_count} tweets sauvegardés")
        print(f"   📊 Engagement total: {stats.get('total_engagement', 0):,}")
        
        return saved_count
    
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return 0


def main():
    parser = argparse.ArgumentParser(description='Scraping Twitter depuis table media')
    parser.add_argument('--media-id', type=int, help='ID d\'un média spécifique')
    parser.add_argument('--all', action='store_true', help='Scraper tous les médias avec Twitter')
    parser.add_argument('--limit', type=int, default=10, 
                       help='Nombre de tweets à récupérer par média (défaut: 10)')
    
    args = parser.parse_args()
    
    # Vérifier le token Twitter
    tw_token = os.getenv('TWITTER_BEARER_TOKEN')
    if not tw_token:
        print("❌ Bearer Token Twitter manquant")
        print("💡 Configurez TWITTER_BEARER_TOKEN dans le fichier .env")
        return
    
    # Initialiser
    print("🔧 Initialisation...")
    db = DatabaseManager()
    tw_scraper = TwitterScraper(tw_token)
    
    # Tester la connexion
    if not tw_scraper.test_connection():
        print("❌ Impossible de se connecter à l'API Twitter")
        return
    
    print("✅ Twitter API connectée\n")
    
    # Scraper un média spécifique
    if args.media_id:
        # Récupérer le média
        medias = db.get_all_medias(actif_only=False)
        media = next((m for m in medias if m.id == args.media_id), None)
        
        if not media:
            print(f"❌ Média ID {args.media_id} non trouvé")
            return
        
        if not media.twitter_account:
            print(f"❌ Aucun compte Twitter configuré pour {media.nom}")
            return
        
        print("="*60)
        print(f"🎯 Scraping: {media.nom}")
        print("="*60)
        
        scrape_twitter_for_media(
            db, tw_scraper, media.id, media.nom,
            media.twitter_account, args.limit
        )
    
    # Scraper tous les médias avec Twitter
    elif args.all:
        print("="*60)
        print("🚀 SCRAPING TWITTER MULTI-MÉDIAS")
        print("="*60)
        
        # Récupérer les médias avec Twitter configuré
        medias = db.get_medias_with_twitter(actif_only=True)
        
        if not medias:
            print("❌ Aucun média avec Twitter configuré")
            print("💡 Ajoutez des comptes Twitter dans la table medias")
            return
        
        print(f"\n📋 {len(medias)} médias à scraper\n")
        
        total_tweets = 0
        
        for i, media in enumerate(medias, 1):
            print(f"[{i}/{len(medias)}] {media.nom}")
            print("-"*60)
            
            count = scrape_twitter_for_media(
                db, tw_scraper, media.id, media.nom,
                media.twitter_account, args.limit
            )
            
            total_tweets += count
        
        # Résumé
        print("\n" + "="*60)
        print("📊 RÉSUMÉ")
        print("="*60)
        print(f"✅ Total tweets: {total_tweets}")
        
        # Afficher le top engagement
        print("\n🏆 TOP ENGAGEMENT TWITTER (30 derniers jours):")
        ranking = db.get_media_ranking_with_twitter(days=30)
        
        for i, media in enumerate(ranking[:5], 1):
            if media['total_tweets'] > 0:
                print(f"\n{i}. {media['nom']}")
                print(f"   Tweets: {media['total_tweets']}")
                print(f"   Retweets: {media['total_retweets']:,}")
                print(f"   Réponses: {media['total_replies']:,}")
                print(f"   Likes: {media['total_likes_tw']:,}")
                print(f"   Quotes: {media['total_quotes']:,}")
                print(f"   Engagement total: {media['engagement_total_tw']:,}")
    
    else:
        print("❌ Spécifiez --media-id ou --all")
        print("💡 Exemples:")
        print("   python scrape_twitter.py --all")
        print("   python scrape_twitter.py --media-id 1 --limit 20")


if __name__ == '__main__':
    main()
