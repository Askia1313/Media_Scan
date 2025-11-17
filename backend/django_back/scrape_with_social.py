#!/usr/bin/env python3
"""
Script de scraping complet : Web + Facebook + Twitter
1. Scrape les articles du site web (RSS/HTML)
2. Classifie automatiquement les articles
3. Scrape les posts Facebook avec métriques d'engagement
4. Scrape les tweets Twitter avec métriques d'engagement
"""

import argparse
import os
from dotenv import load_dotenv
from database.db_manager import DatabaseManager
from scrapers.scraper_manager import ScraperManager
from scrapers.facebook_scraper import FacebookScraper
from scrapers.twitter_scraper import TwitterScraper

# Charger les variables d'environnement
load_dotenv()


def load_config_file(file_path: str) -> dict:
    """
    [DEPRECATED] Charger un fichier de configuration
    Conservé pour compatibilité mais non utilisé
    
    Returns:
        Dictionnaire {url_site: identifiant}
    """
    return {}


def scrape_facebook_for_media(db: DatabaseManager, fb_scraper: FacebookScraper, 
                              media_id: int, fb_page: str, limit: int = 5):
    """Scraper Facebook pour un média"""
    print(f"\n📘 Scraping Facebook: {fb_page}")
    
    try:
        result = fb_scraper.scrape_page(fb_page, limit=limit)
        
        if result.get('error'):
            print(f"   ❌ Erreur: {result['error']}")
            return
        
        posts = result.get('posts', [])
        
        if not posts:
            print(f"   ⚠️ Aucun post récupéré")
            return
        
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
        print(f"   📊 Engagement: {stats.get('total_engagement', 0):,}")
    
    except Exception as e:
        print(f"   ❌ Erreur: {e}")


def scrape_twitter_for_media(db: DatabaseManager, tw_scraper: TwitterScraper,
                             media_id: int, tw_account: str, limit: int = 5):
    """Scraper Twitter pour un média"""
    print(f"\n🐦 Scraping Twitter: @{tw_account}")
    
    try:
        result = tw_scraper.scrape_user(tw_account, max_results=limit)
        
        if result.get('error'):
            print(f"   ❌ Erreur: {result['error']}")
            return
        
        tweets = result.get('tweets', [])
        
        if not tweets:
            print(f"   ⚠️ Aucun tweet récupéré")
            return
        
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
        print(f"   📊 Engagement: {stats.get('total_engagement', 0):,}")
    
    except Exception as e:
        print(f"   ❌ Erreur: {e}")


def main():
    parser = argparse.ArgumentParser(description='Scraping Web + Facebook + Twitter')
    parser.add_argument('--url', type=str, help='URL d\'un média spécifique')
    parser.add_argument('--all', action='store_true', help='Scraper tous les sites')
    parser.add_argument('--days', type=int, default=30, help='Nombre de jours à scraper')
    parser.add_argument('--fb-posts', type=int, default=5, 
                       help='Nombre de posts Facebook à récupérer')
    parser.add_argument('--tweets', type=int, default=5,
                       help='Nombre de tweets à récupérer')
    parser.add_argument('--skip-facebook', action='store_true',
                       help='Ignorer le scraping Facebook')
    parser.add_argument('--skip-twitter', action='store_true',
                       help='Ignorer le scraping Twitter')
    
    args = parser.parse_args()
    
    # Initialiser
    print("🔧 Initialisation...")
    db = DatabaseManager()
    scraper_manager = ScraperManager(db, auto_classify=True)
    
    # Initialiser le scraper Facebook
    fb_scraper = None
    if not args.skip_facebook:
        fb_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        if fb_token:
            fb_scraper = FacebookScraper(fb_token)
            if fb_scraper.test_connection():
                print("✅ Facebook API connectée")
            else:
                print("⚠️ Facebook API non accessible")
                fb_scraper = None
        else:
            print("⚠️ Token Facebook manquant")
    
    # Initialiser le scraper Twitter
    tw_scraper = None
    if not args.skip_twitter:
        tw_token = os.getenv('TWITTER_BEARER_TOKEN')
        if tw_token:
            tw_scraper = TwitterScraper(tw_token)
            if tw_scraper.test_connection():
                print("✅ Twitter API connectée")
            else:
                print("⚠️ Twitter API non accessible")
                tw_scraper = None
        else:
            print("⚠️ Bearer Token Twitter manquant")
    
    print()
    
    # Scraper un site spécifique
    if args.url:
        print("="*60)
        print(f"🎯 Scraping: {args.url}")
        print("="*60)
        
        # Scraping web
        count, method, message = scraper_manager.scrape_site(args.url, days=args.days)
        print(message)
        
        # Récupérer le média
        media = db.get_media_by_url(args.url)
        if media:
            # Scraping Facebook
            if fb_scraper and media.facebook_page:
                scrape_facebook_for_media(
                    db, fb_scraper, media.id, 
                    media.facebook_page, args.fb_posts
                )
            
            # Scraping Twitter
            if tw_scraper and media.twitter_account:
                scrape_twitter_for_media(
                    db, tw_scraper, media.id,
                    media.twitter_account, args.tweets
                )
    
    # Scraper tous les sites
    elif args.all:
        print("="*60)
        print("🚀 SCRAPING MULTI-SITES (depuis table media)")
        print("="*60)
        
        # Récupérer tous les médias actifs
        medias = db.get_all_medias(actif_only=True)
        
        if not medias:
            print("❌ Aucun média trouvé dans la table media")
            return
        
        total_articles = 0
        
        for i, media in enumerate(medias, 1):
            print(f"\n[{i}/{len(medias)}] {media.nom} ({media.url})")
            print("-"*60)
            
            # Scraping web
            if media.url:
                count, method, message = scraper_manager.scrape_site(media.url, days=args.days)
                total_articles += count
                print(f"   {message}")
            
            # Scraping Facebook
            if fb_scraper and media.facebook_page:
                scrape_facebook_for_media(
                    db, fb_scraper, media.id,
                    media.facebook_page, args.fb_posts
                )
            
            # Scraping Twitter
            if tw_scraper and media.twitter_account:
                scrape_twitter_for_media(
                    db, tw_scraper, media.id,
                    media.twitter_account, args.tweets
                )
        
        # Résumé
        print("\n" + "="*60)
        print("📊 RÉSUMÉ")
        print("="*60)
        print(f"✅ Total articles: {total_articles}")
        
        # Afficher le classement
        print("\n" + "="*60)
        print("🏆 CLASSEMENT DES MÉDIAS")
        print("="*60 + "\n")
        
        ranking = db.get_media_ranking_with_twitter(days=args.days)
        for i, media in enumerate(ranking[:5], 1):
            print(f"{i}. {media['nom']}")
            print(f"   Articles: {media['total_articles']}")
            if media['total_posts_facebook'] > 0:
                print(f"   Facebook: {media['engagement_total_fb']:,}")
            if media['total_tweets'] > 0:
                print(f"   Twitter: {media['engagement_total_tw']:,}")
            if media['engagement_total'] > 0:
                print(f"   Total: {media['engagement_total']:,}")
            print()
        
        # Lancer la modération de contenu
        print("\n" + "="*60)
        print("🛡️ MODÉRATION DE CONTENU")
        print("="*60 + "\n")
        
        try:
            from analysis.content_moderator import ContentModerator
            
            moderator = ContentModerator()
            
            # Vérifier la connexion à Ollama
            if not moderator.check_ollama_status():
                print("⚠️ Ollama non disponible, modération ignorée")
            else:
                print("✅ Ollama connecté, lancement de la modération...\n")
                
                # Modérer les articles
                articles = db.get_recent_articles(days=args.days, limit=1000)
                analyzed = 0
                flagged = 0
                
                for article in articles:
                    # Vérifier si déjà analysé
                    existing = db.get_content_moderation('article', article.id)
                    if existing:
                        continue
                    
                    text = f"{article.titre}\n\n{article.contenu or article.extrait or ''}"
                    analysis = moderator.analyze_content(text, 'article')
                    db.add_content_moderation('article', article.id, analysis)
                    
                    analyzed += 1
                    if analysis['should_flag']:
                        flagged += 1
                        print(f"🚨 Article {article.id} signalé - {analysis['risk_level']} (Score: {analysis['risk_score']})")
                
                # Modérer les posts Facebook
                if not args.skip_facebook:
                    posts = db.get_recent_facebook_posts(days=args.days, limit=500)
                    for post in posts:
                        existing = db.get_content_moderation('facebook_post', post.id)
                        if existing:
                            continue
                        
                        text = post.message or ""
                        if text.strip():
                            analysis = moderator.analyze_content(text, 'facebook_post')
                            db.add_content_moderation('facebook_post', post.id, analysis)
                            analyzed += 1
                            if analysis['should_flag']:
                                flagged += 1
                
                # Modérer les tweets
                if not args.skip_twitter:
                    tweets = db.get_recent_twitter_tweets(days=args.days, limit=500)
                    for tweet in tweets:
                        existing = db.get_content_moderation('tweet', tweet.id)
                        if existing:
                            continue
                        
                        text = tweet.text or ""
                        if text.strip():
                            analysis = moderator.analyze_content(text, 'tweet')
                            db.add_content_moderation('tweet', tweet.id, analysis)
                            analyzed += 1
                            if analysis['should_flag']:
                                flagged += 1
                
                print(f"\n✅ Modération terminée:")
                print(f"   Contenus analysés: {analyzed}")
                print(f"   Contenus signalés: {flagged}")
                if analyzed > 0:
                    print(f"   Taux de signalement: {(flagged/analyzed)*100:.1f}%")
        
        except Exception as e:
            print(f"⚠️ Erreur lors de la modération: {e}")
            print("   Le scraping a réussi mais la modération a échoué")
    
    else:
        print("❌ Spécifiez --url ou --all")
        print("💡 Exemples:")
        print("   python scrape_with_social.py --url https://www.aib.media")
        print("   python scrape_with_social.py --all")
        print("   python scrape_with_social.py --all --skip-facebook")


if __name__ == '__main__':
    main()
