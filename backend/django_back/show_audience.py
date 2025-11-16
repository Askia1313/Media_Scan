#!/usr/bin/env python3
"""
Afficher l'analyse d'audience par plateforme
"""

import argparse
from database.db_manager import DatabaseManager
from analysis.audience_analyzer import AudienceAnalyzer


def print_separator(char="=", length=80):
    """Affiche un séparateur"""
    print(char * length)


def print_web_audience(analyzer: AudienceAnalyzer, days: int):
    """Affiche l'audience Web"""
    print_separator()
    print(f"📰 AUDIENCE WEB - ARTICLES ({days} derniers jours)")
    print_separator()
    print()
    
    medias = analyzer.analyze_web_audience(days)
    
    if not medias:
        print("⚠️ Aucune donnée disponible")
        return
    
    for i, media in enumerate(medias, 1):
        print(f"{i}. 📺 {media['nom']}")
        print(f"   {'─' * 70}")
        print(f"   🌐 URL: {media['url']}")
        print(f"   📊 Volume: {media['total_articles']} articles")
        print(f"   📅 Jours avec publication: {media['jours_avec_publication']}")
        print(f"   📈 Moyenne: {media['articles_par_jour_moyen']} articles/jour (jours actifs)")
        
        if media['derniere_publication']:
            print(f"   📅 Dernière publication: {media['derniere_publication'][:10]}")
            print(f"   ⏱️ Il y a {media['jours_depuis_derniere_pub']} jour(s)")
        else:
            print(f"   ❌ Aucune publication")
        
        print(f"   {media['statut']}")
        print()


def print_facebook_audience(analyzer: AudienceAnalyzer, days: int):
    """Affiche l'audience Facebook"""
    print_separator()
    print(f"📘 AUDIENCE FACEBOOK ({days} derniers jours)")
    print_separator()
    print()
    
    medias = analyzer.analyze_facebook_audience(days)
    
    if not medias:
        print("⚠️ Aucune donnée disponible")
        return
    
    for i, media in enumerate(medias, 1):
        print(f"{i}. 📺 {media['nom']}")
        print(f"   {'─' * 70}")
        print(f"   📘 Page: {media['facebook_page']}")
        print(f"   📊 Volume: {media['total_posts']} posts")
        print(f"   📅 Jours avec publication: {media['jours_avec_publication']}")
        print(f"   📈 Moyenne: {media['posts_par_jour_moyen']} posts/jour (jours actifs)")
        
        if media['total_posts'] > 0:
            print(f"   👍 Likes: {media['total_likes']:,}")
            print(f"   💬 Commentaires: {media['total_comments']:,}")
            print(f"   🔄 Partages: {media['total_shares']:,}")
            print(f"   📊 Engagement total: {media['engagement_total']:,}")
            print(f"   📈 Engagement moyen: {media['engagement_moyen']:.0f} par post")
        
        if media['derniere_publication']:
            print(f"   📅 Dernière publication: {media['derniere_publication'][:10]}")
            print(f"   ⏱️ Il y a {media['jours_depuis_derniere_pub']} jour(s)")
        else:
            print(f"   ❌ Aucune publication")
        
        print(f"   {media['statut']}")
        print()


def print_twitter_audience(analyzer: AudienceAnalyzer, days: int):
    """Affiche l'audience Twitter"""
    print_separator()
    print(f"🐦 AUDIENCE TWITTER ({days} derniers jours)")
    print_separator()
    print()
    
    medias = analyzer.analyze_twitter_audience(days)
    
    if not medias:
        print("⚠️ Aucune donnée disponible")
        return
    
    for i, media in enumerate(medias, 1):
        print(f"{i}. 📺 {media['nom']}")
        print(f"   {'─' * 70}")
        print(f"   🐦 Compte: @{media['twitter_account']}")
        print(f"   📊 Volume: {media['total_tweets']} tweets")
        print(f"   📅 Jours avec publication: {media['jours_avec_publication']}")
        print(f"   📈 Moyenne: {media['tweets_par_jour_moyen']} tweets/jour (jours actifs)")
        
        if media['total_tweets'] > 0:
            print(f"   🔄 Retweets: {media['total_retweets']:,}")
            print(f"   💬 Réponses: {media['total_replies']:,}")
            print(f"   ❤️ Likes: {media['total_likes']:,}")
            print(f"   💭 Citations: {media['total_quotes']:,}")
            if media['total_impressions'] > 0:
                print(f"   👁️ Impressions: {media['total_impressions']:,}")
            print(f"   📊 Engagement total: {media['engagement_total']:,}")
            print(f"   📈 Engagement moyen: {media['engagement_moyen']:.0f} par tweet")
        
        if media['derniere_publication']:
            print(f"   📅 Dernière publication: {media['derniere_publication'][:10]}")
            print(f"   ⏱️ Il y a {media['jours_depuis_derniere_pub']} jour(s)")
        else:
            print(f"   ❌ Aucune publication")
        
        print(f"   {media['statut']}")
        print()


def print_global_audience(analyzer: AudienceAnalyzer, days: int):
    """Affiche l'audience globale"""
    print_separator()
    print(f"🏆 CLASSEMENT GLOBAL PAR INFLUENCE ({days} derniers jours)")
    print_separator()
    print()
    
    medias = analyzer.analyze_global_audience(days)
    
    if not medias:
        print("⚠️ Aucune donnée disponible")
        return
    
    for i, media in enumerate(medias, 1):
        emoji = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
        
        print(f"{emoji} 📺 {media['nom']}")
        print(f"   {'─' * 70}")
        print(f"   🌐 URL: {media['url']}")
        print(f"   🎯 Score d'influence: {media['score_influence']:.2f}")
        print()
        
        # Web
        web = media['web']
        if web:
            print(f"   📰 Web: {web.get('total_articles', 0)} articles")
            print(f"      Fréquence: {web.get('articles_par_jour', 0)} articles/jour")
        
        # Facebook
        fb = media['facebook']
        if fb and fb.get('total_posts', 0) > 0:
            print(f"   📘 Facebook: {fb['total_posts']} posts")
            print(f"      Engagement: {fb['engagement_total']:,}")
        
        # Twitter
        tw = media['twitter']
        if tw and tw.get('total_tweets', 0) > 0:
            print(f"   🐦 Twitter: {tw['total_tweets']} tweets")
            print(f"      Engagement: {tw['engagement_total']:,}")
        
        print(f"   📊 Publications totales: {media['total_publications']}")
        print(f"   📈 Engagement total: {media['total_engagement']:,}")
        print()


def print_inactive_medias(analyzer: AudienceAnalyzer, days_threshold: int):
    """Affiche les médias inactifs"""
    print_separator()
    print(f"🔴 MÉDIAS INACTIFS (>{days_threshold} jours sans publication)")
    print_separator()
    print()
    
    inactive = analyzer.get_inactive_medias(days_threshold)
    
    # Web
    if inactive['web']:
        print(f"📰 WEB ({len(inactive['web'])} médias):")
        for media in inactive['web']:
            print(f"   • {media['nom']}: {media['jours_depuis_derniere_pub']} jours")
        print()
    
    # Facebook
    if inactive['facebook']:
        print(f"📘 FACEBOOK ({len(inactive['facebook'])} médias):")
        for media in inactive['facebook']:
            print(f"   • {media['nom']}: {media['jours_depuis_derniere_pub']} jours")
        print()
    
    # Twitter
    if inactive['twitter']:
        print(f"🐦 TWITTER ({len(inactive['twitter'])} médias):")
        for media in inactive['twitter']:
            print(f"   • {media['nom']}: {media['jours_depuis_derniere_pub']} jours")
        print()
    
    if not (inactive['web'] or inactive['facebook'] or inactive['twitter']):
        print("✅ Tous les médias sont actifs !")
        print()


def main():
    parser = argparse.ArgumentParser(description='Analyse d\'audience par plateforme')
    parser.add_argument('--platform', type=str, choices=['web', 'facebook', 'twitter', 'global', 'all'],
                       default='all', help='Plateforme à analyser')
    parser.add_argument('--days', type=int, default=30,
                       help='Période d\'analyse en jours (défaut: 30)')
    parser.add_argument('--inactive', type=int,
                       help='Afficher les médias inactifs (nombre de jours)')
    
    args = parser.parse_args()
    
    print()
    print("🔧 Initialisation de l'analyse...")
    db = DatabaseManager()
    analyzer = AudienceAnalyzer(db)
    print()
    
    # Afficher selon la plateforme
    if args.platform == 'web' or args.platform == 'all':
        print_web_audience(analyzer, args.days)
    
    if args.platform == 'facebook' or args.platform == 'all':
        print_facebook_audience(analyzer, args.days)
    
    if args.platform == 'twitter' or args.platform == 'all':
        print_twitter_audience(analyzer, args.days)
    
    if args.platform == 'global' or args.platform == 'all':
        print_global_audience(analyzer, args.days)
    
    # Afficher les médias inactifs
    if args.inactive:
        print_inactive_medias(analyzer, args.inactive)
    
    print_separator()
    print("✅ Analyse terminée")
    print_separator()


if __name__ == '__main__':
    main()
