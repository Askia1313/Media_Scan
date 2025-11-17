"""
Script pour analyser et modérer les contenus (articles, posts Facebook, tweets)
Détecte: toxicité, fake news, discours sensibles
"""

import argparse
from database.db_manager import DatabaseManager
from analysis.content_moderator import ContentModerator


def moderate_articles(db: DatabaseManager, moderator: ContentModerator, limit: int = 10):
    """
    Modère les articles récents
    
    Args:
        db: Gestionnaire de base de données
        moderator: Modérateur de contenu
        limit: Nombre d'articles à analyser
    """
    print(f"\n📰 Analyse des articles...")
    print("=" * 80)
    
    articles = db.get_recent_articles(days=7, limit=limit)
    
    if not articles:
        print("⚠️ Aucun article à analyser")
        return
    
    analyzed = 0
    flagged = 0
    
    for article in articles:
        # Vérifier si déjà analysé
        existing = db.get_content_moderation('article', article.id)
        if existing:
            print(f"⏭️ Article {article.id} déjà analysé")
            continue
        
        print(f"\n🔍 Analyse de l'article {article.id}: {article.titre[:50]}...")
        
        # Analyser le contenu
        text = f"{article.titre}\n\n{article.contenu or article.extrait or ''}"
        analysis = moderator.analyze_content(text, 'article')
        
        # Sauvegarder l'analyse
        db.add_content_moderation('article', article.id, analysis)
        
        analyzed += 1
        if analysis['should_flag']:
            flagged += 1
            print(f"   🚨 SIGNALÉ - {analysis['risk_level']} (Score: {analysis['risk_score']})")
            
            flags = []
            if analysis['toxicity']['est_toxique']:
                flags.append(f"Toxicité: {analysis['toxicity']['score_toxicite']}/10")
            if analysis['misinformation']['est_desinformation']:
                flags.append(f"Désinformation: {analysis['misinformation']['score_desinformation']}/10")
            if analysis['sensitivity']['est_sensible']:
                flags.append(f"Sensibilité: {analysis['sensitivity']['score_sensibilite']}/10")
            
            if flags:
                print(f"      ⚠️ {' | '.join(flags)}")
        else:
            print(f"   ✅ OK - {analysis['risk_level']} (Score: {analysis['risk_score']})")
    
    print(f"\n📊 Résumé:")
    print(f"   Articles analysés: {analyzed}")
    print(f"   Articles signalés: {flagged}")
    if analyzed > 0:
        print(f"   Taux de signalement: {(flagged/analyzed)*100:.1f}%")


def moderate_facebook_posts(db: DatabaseManager, moderator: ContentModerator, media_id: int = None, limit: int = 10):
    """
    Modère les posts Facebook
    
    Args:
        db: Gestionnaire de base de données
        moderator: Modérateur de contenu
        media_id: ID du média (optionnel)
        limit: Nombre de posts à analyser
    """
    print(f"\n📘 Analyse des posts Facebook...")
    print("=" * 80)
    
    if media_id:
        posts = db.get_facebook_posts_by_media(media_id, limit=limit)
    else:
        # Récupérer les posts de tous les médias
        medias = db.get_all_medias()
        posts = []
        for media in medias[:3]:  # Limiter à 3 médias
            posts.extend(db.get_facebook_posts_by_media(media.id, limit=5))
    
    if not posts:
        print("⚠️ Aucun post Facebook à analyser")
        return
    
    analyzed = 0
    flagged = 0
    
    for post in posts:
        # Vérifier si déjà analysé
        existing = db.get_content_moderation('facebook_post', post['id'])
        if existing:
            print(f"⏭️ Post {post['id']} déjà analysé")
            continue
        
        message = post.get('message', '')
        if not message or len(message) < 10:
            continue
        
        print(f"\n🔍 Analyse du post {post['id']}: {message[:50]}...")
        
        # Analyser le contenu
        analysis = moderator.analyze_content(message, 'facebook_post')
        
        # Sauvegarder l'analyse
        db.add_content_moderation('facebook_post', post['id'], analysis)
        
        analyzed += 1
        if analysis['should_flag']:
            flagged += 1
            print(f"   🚨 SIGNALÉ - {analysis['risk_level']} (Score: {analysis['risk_score']})")
        else:
            print(f"   ✅ OK - {analysis['risk_level']} (Score: {analysis['risk_score']})")
    
    print(f"\n📊 Résumé:")
    print(f"   Posts analysés: {analyzed}")
    print(f"   Posts signalés: {flagged}")
    if analyzed > 0:
        print(f"   Taux de signalement: {(flagged/analyzed)*100:.1f}%")


def moderate_tweets(db: DatabaseManager, moderator: ContentModerator, media_id: int = None, limit: int = 10):
    """
    Modère les tweets
    
    Args:
        db: Gestionnaire de base de données
        moderator: Modérateur de contenu
        media_id: ID du média (optionnel)
        limit: Nombre de tweets à analyser
    """
    print(f"\n🐦 Analyse des tweets...")
    print("=" * 80)
    
    if media_id:
        tweets = db.get_twitter_tweets_by_media(media_id, limit=limit)
    else:
        # Récupérer les tweets de tous les médias
        medias = db.get_all_medias()
        tweets = []
        for media in medias[:3]:  # Limiter à 3 médias
            tweets.extend(db.get_twitter_tweets_by_media(media.id, limit=5))
    
    if not tweets:
        print("⚠️ Aucun tweet à analyser")
        return
    
    analyzed = 0
    flagged = 0
    
    for tweet in tweets:
        # Vérifier si déjà analysé
        existing = db.get_content_moderation('tweet', tweet['id'])
        if existing:
            print(f"⏭️ Tweet {tweet['id']} déjà analysé")
            continue
        
        text = tweet.get('text', '')
        if not text or len(text) < 10:
            continue
        
        print(f"\n🔍 Analyse du tweet {tweet['id']}: {text[:50]}...")
        
        # Analyser le contenu
        analysis = moderator.analyze_content(text, 'tweet')
        
        # Sauvegarder l'analyse
        db.add_content_moderation('tweet', tweet['id'], analysis)
        
        analyzed += 1
        if analysis['should_flag']:
            flagged += 1
            print(f"   🚨 SIGNALÉ - {analysis['risk_level']} (Score: {analysis['risk_score']})")
        else:
            print(f"   ✅ OK - {analysis['risk_level']} (Score: {analysis['risk_score']})")
    
    print(f"\n📊 Résumé:")
    print(f"   Tweets analysés: {analyzed}")
    print(f"   Tweets signalés: {flagged}")
    if analyzed > 0:
        print(f"   Taux de signalement: {(flagged/analyzed)*100:.1f}%")


def show_flagged_contents(db: DatabaseManager):
    """
    Affiche les contenus signalés
    
    Args:
        db: Gestionnaire de base de données
    """
    print(f"\n🚨 Contenus signalés")
    print("=" * 80)
    
    flagged = db.get_flagged_contents(limit=50)
    
    if not flagged:
        print("✅ Aucun contenu signalé")
        return
    
    for item in flagged:
        print(f"\n{item['risk_level']} - {item['content_type'].upper()} #{item['content_id']}")
        print(f"   Score de risque: {item['risk_score']}/10")
        
        flags = []
        if item['is_toxic']:
            flags.append("Toxique")
        if item['is_misinformation']:
            flags.append("Désinformation")
        if item['is_sensitive']:
            flags.append("Sensible")
        
        print(f"   Signalements: {', '.join(flags)}")
        print(f"   Analysé le: {item['analyzed_at']}")


def show_stats(db: DatabaseManager):
    """
    Affiche les statistiques de modération
    
    Args:
        db: Gestionnaire de base de données
    """
    print(f"\n📊 Statistiques de modération")
    print("=" * 80)
    
    stats = db.get_moderation_stats()
    
    print(f"Total analysé: {stats['total_analyzed']}")
    print(f"Total signalé: {stats['total_flagged']}")
    print(f"Contenus toxiques: {stats['total_toxic']}")
    print(f"Désinformation: {stats['total_misinformation']}")
    print(f"Contenus sensibles: {stats['total_sensitive']}")
    print(f"Score de risque moyen: {stats['avg_risk_score']}/10")
    
    if stats['total_analyzed'] > 0:
        print(f"\nTaux de signalement: {(stats['total_flagged']/stats['total_analyzed'])*100:.1f}%")


def main():
    parser = argparse.ArgumentParser(description='Modération de contenu avec Ollama')
    parser.add_argument('--type', choices=['articles', 'facebook', 'twitter', 'all'], 
                       default='all', help='Type de contenu à analyser')
    parser.add_argument('--limit', type=int, default=10, help='Nombre de contenus à analyser')
    parser.add_argument('--media-id', type=int, help='ID du média à analyser')
    parser.add_argument('--show-flagged', action='store_true', help='Afficher les contenus signalés')
    parser.add_argument('--stats', action='store_true', help='Afficher les statistiques')
    parser.add_argument('--test', action='store_true', help='Tester la connexion à Ollama')
    
    args = parser.parse_args()
    
    # Initialiser
    db = DatabaseManager()
    moderator = ContentModerator()
    
    print("🔧 Initialisation du modérateur de contenu...")
    
    # Test de connexion
    if args.test or args.type != 'none':
        if not moderator.test_connection():
            print("\n❌ Impossible de se connecter à Ollama")
            print("💡 Lancez Ollama avec: ollama serve")
            print("💡 Téléchargez le modèle avec: ollama pull llama3.2")
            return
    
    # Afficher les statistiques
    if args.stats:
        show_stats(db)
        return
    
    # Afficher les contenus signalés
    if args.show_flagged:
        show_flagged_contents(db)
        return
    
    # Analyser les contenus
    if args.type in ['articles', 'all']:
        moderate_articles(db, moderator, args.limit)
    
    if args.type in ['facebook', 'all']:
        moderate_facebook_posts(db, moderator, args.media_id, args.limit)
    
    if args.type in ['twitter', 'all']:
        moderate_tweets(db, moderator, args.media_id, args.limit)
    
    # Afficher les statistiques finales
    print("\n" + "=" * 80)
    show_stats(db)
    
    print("\n✅ Modération terminée")


if __name__ == "__main__":
    main()
