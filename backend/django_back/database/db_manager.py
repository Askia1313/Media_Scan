"""
Gestionnaire de base de données SQLite
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pathlib import Path

from .models import Article, Media


class DatabaseManager:
    """Gestionnaire de la base de données SQLite"""
    
    def __init__(self, db_path: str = 'data/media_scan.db'):
        """
        Initialise le gestionnaire de base de données
        
        Args:
            db_path: Chemin vers le fichier de base de données
        """
        self.db_path = db_path
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialiser la base de données
        self._init_database()
    
    def _init_database(self):
        """Initialise la base de données avec le schéma"""
        schema_path = Path(__file__).parent / 'schema.sql'
        
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()
        
        conn = self.get_connection()
        try:
            conn.executescript(schema)
            conn.commit()
        finally:
            conn.close()
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Crée une nouvelle connexion à la base de données
        
        Returns:
            Connexion SQLite avec row_factory configuré
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # ==================== MÉDIAS ====================
    
    def add_media(self, nom: str, url: str, type_site: str = 'unknown') -> int:
        """
        Ajoute ou met à jour un média
        
        Args:
            nom: Nom du média
            url: URL du site
            type_site: Type de site (wordpress, html, rss)
            
        Returns:
            ID du média
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO medias (nom, url, type_site)
                VALUES (?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    nom = excluded.nom,
                    type_site = excluded.type_site
            """, (nom, url, type_site))
            
            media_id = cursor.lastrowid
            
            # Si c'était un UPDATE, récupérer l'ID existant
            if media_id == 0:
                cursor.execute("SELECT id FROM medias WHERE url = ?", (url,))
                media_id = cursor.fetchone()[0]
            
            conn.commit()
            return media_id
        
        finally:
            conn.close()
    
    def get_media_by_url(self, url: str) -> Optional[Media]:
        """Récupérer un média par son URL"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM medias WHERE url = ?", (url,))
            row = cursor.fetchone()
            
            if row:
                return Media(
                    id=row['id'],
                    nom=row['nom'],
                    url=row['url'],
                    type_site=row['type_site'],
                    actif=bool(row['actif']),
                    derniere_collecte=row['derniere_collecte'],
                    created_at=row['created_at']
                )
            return None
        
        finally:
            conn.close()
    
    def get_all_medias(self, actif_only: bool = True) -> List[Media]:
        """Récupérer tous les médias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if actif_only:
                cursor.execute("SELECT * FROM medias WHERE actif = 1 ORDER BY nom")
            else:
                cursor.execute("SELECT * FROM medias ORDER BY nom")
            
            medias = []
            for row in cursor.fetchall():
                medias.append(Media(
                    id=row['id'],
                    nom=row['nom'],
                    url=row['url'],
                    type_site=row['type_site'],
                    actif=bool(row['actif']),
                    derniere_collecte=row['derniere_collecte'],
                    created_at=row['created_at']
                ))
            
            return medias
        
        finally:
            conn.close()
    
    def update_media_last_scrape(self, media_id: int):
        """Met à jour la date de dernière collecte d'un média"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE medias 
                SET derniere_collecte = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (media_id,))
            conn.commit()
        
        finally:
            conn.close()
    
    # ==================== ARTICLES ====================
    
    def add_article(self, article: Article) -> int:
        """
        Ajoute un article à la base de données
        
        Args:
            article: Instance d'Article
            
        Returns:
            ID de l'article inséré, ou 0 si déjà existant
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO articles (
                    media_id, titre, contenu, extrait, url, auteur,
                    date_publication, image_url, categories, tags,
                    source_type, vues, commentaires
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(url) DO NOTHING
            """, (
                article.media_id,
                article.titre,
                article.contenu,
                article.extrait,
                article.url,
                article.auteur,
                article.date_publication,
                article.image_url,
                json.dumps(article.categories) if article.categories else None,
                json.dumps(article.tags) if article.tags else None,
                article.source_type,
                article.vues,
                article.commentaires
            ))
            
            article_id = cursor.lastrowid
            conn.commit()
            
            return article_id
        
        except sqlite3.IntegrityError:
            return 0
        
        finally:
            conn.close()
    
    def get_article_by_url(self, url: str) -> Optional[Article]:
        """Récupérer un article par son URL"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM articles WHERE url = ?", (url,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_article(row)
            return None
        
        finally:
            conn.close()
    
    def get_articles_by_media(self, media_id: int, limit: int = 100) -> List[Article]:
        """Récupérer les articles d'un média"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM articles 
                WHERE media_id = ?
                ORDER BY date_publication DESC
                LIMIT ?
            """, (media_id, limit))
            
            return [self._row_to_article(row) for row in cursor.fetchall()]
        
        finally:
            conn.close()
    
    def get_recent_articles(self, days: int = 7, limit: int = 100) -> List[Article]:
        """Récupérer les articles récents"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            date_limit = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute("""
                SELECT * FROM articles 
                WHERE date_publication >= ?
                ORDER BY date_publication DESC
                LIMIT ?
            """, (date_limit, limit))
            
            return [self._row_to_article(row) for row in cursor.fetchall()]
        
        finally:
            conn.close()
    
    def _row_to_article(self, row: sqlite3.Row) -> Article:
        """Convertit une ligne SQL en objet Article"""
        return Article(
            id=row['id'],
            media_id=row['media_id'],
            titre=row['titre'],
            contenu=row['contenu'],
            extrait=row['extrait'],
            url=row['url'],
            auteur=row['auteur'],
            date_publication=row['date_publication'],
            image_url=row['image_url'],
            categories=json.loads(row['categories']) if row['categories'] else [],
            tags=json.loads(row['tags']) if row['tags'] else [],
            source_type=row['source_type'],
            vues=row['vues'],
            commentaires=row['commentaires'],
            scraped_at=row['scraped_at'],
            created_at=row['created_at']
        )
    
    # ==================== LOGS ====================
    
    def add_scraping_log(self, media_id: int, status: str, methode: str, 
                        articles_collectes: int = 0, message: str = ""):
        """Ajoute un log de scraping"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO scraping_logs (media_id, status, methode, articles_collectes, message)
                VALUES (?, ?, ?, ?, ?)
            """, (media_id, status, methode, articles_collectes, message))
            
            conn.commit()
        
        finally:
            conn.close()
    
    # ==================== CLASSIFICATIONS ====================
    
    def add_classification(self, article_id: int, categorie: str, confiance: float,
                          mots_cles: List[str] = None, justification: str = "",
                          methode: str = "mistral_ollama"):
        """Ajoute une classification thématique"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO classifications (
                    article_id, categorie, confiance, mots_cles, justification, methode
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(article_id) DO UPDATE SET
                    categorie = excluded.categorie,
                    confiance = excluded.confiance,
                    mots_cles = excluded.mots_cles,
                    justification = excluded.justification,
                    methode = excluded.methode,
                    created_at = CURRENT_TIMESTAMP
            """, (
                article_id,
                categorie,
                confiance,
                json.dumps(mots_cles) if mots_cles else None,
                justification,
                methode
            ))
            
            conn.commit()
        
        finally:
            conn.close()
    
    def get_classification(self, article_id: int) -> Optional[Dict[str, Any]]:
        """Récupère la classification d'un article"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM classifications WHERE article_id = ?
            """, (article_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'article_id': row['article_id'],
                    'categorie': row['categorie'],
                    'confiance': row['confiance'],
                    'mots_cles': json.loads(row['mots_cles']) if row['mots_cles'] else [],
                    'justification': row['justification'],
                    'methode': row['methode'],
                    'created_at': row['created_at']
                }
            return None
        
        finally:
            conn.close()
    
    def get_articles_by_category(self, categorie: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupère les articles d'une catégorie"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT a.*, c.categorie, c.confiance
                FROM articles a
                JOIN classifications c ON a.id = c.article_id
                WHERE c.categorie = ?
                ORDER BY a.date_publication DESC
                LIMIT ?
            """, (categorie, limit))
            
            results = []
            for row in cursor.fetchall():
                article = self._row_to_article(row)
                results.append({
                    'article': article,
                    'categorie': row['categorie'],
                    'confiance': row['confiance']
                })
            
            return results
        
        finally:
            conn.close()
    
    def get_category_stats(self, days: int = 30) -> List[Dict[str, Any]]:
        """Statistiques par catégorie"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            date_limit = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute("""
                SELECT 
                    c.categorie,
                    COUNT(*) as total,
                    AVG(c.confiance) as confiance_moyenne
                FROM classifications c
                JOIN articles a ON c.article_id = a.id
                WHERE a.date_publication >= ?
                GROUP BY c.categorie
                ORDER BY total DESC
            """, (date_limit,))
            
            return [dict(row) for row in cursor.fetchall()]
        
        finally:
            conn.close()
    
    # ==================== FACEBOOK ====================
    
    def add_facebook_post(self, media_id: int, post_id: str, message: str,
                         url: str, image_url: str = None, date_publication: str = None,
                         likes: int = 0, comments: int = 0, shares: int = 0) -> int:
        """Ajoute ou met à jour un post Facebook"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        engagement_total = likes + comments + shares
        
        try:
            cursor.execute("""
                INSERT INTO facebook_posts (
                    media_id, post_id, message, url, image_url, date_publication,
                    likes, comments, shares, engagement_total
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(post_id) DO UPDATE SET
                    likes = excluded.likes,
                    comments = excluded.comments,
                    shares = excluded.shares,
                    engagement_total = excluded.engagement_total,
                    scraped_at = CURRENT_TIMESTAMP
            """, (
                media_id, post_id, message, url, image_url, date_publication,
                likes, comments, shares, engagement_total
            ))
            
            post_id_db = cursor.lastrowid
            conn.commit()
            
            return post_id_db
        
        finally:
            conn.close()
    
    def get_facebook_posts_by_media(self, media_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupère les posts Facebook d'un média"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM facebook_posts
                WHERE media_id = ?
                ORDER BY date_publication DESC
                LIMIT ?
            """, (media_id, limit))
            
            return [dict(row) for row in cursor.fetchall()]
        
        finally:
            conn.close()
    
    def calculate_media_metrics(self, media_id: int, days: int = 30) -> Optional[Dict[str, Any]]:
        """Calcule les métriques d'un média"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            date_limit = (datetime.now() - timedelta(days=days)).isoformat()
            periode_debut = date_limit
            periode_fin = datetime.now().isoformat()
            
            # Compter les articles
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM articles
                WHERE media_id = ? AND date_publication >= ?
            """, (media_id, date_limit))
            
            total_articles = cursor.fetchone()['total']
            
            # Métriques Facebook
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_posts,
                    SUM(likes) as total_likes,
                    SUM(comments) as total_comments,
                    SUM(shares) as total_shares,
                    SUM(engagement_total) as engagement_total,
                    AVG(engagement_total) as engagement_moyen
                FROM facebook_posts
                WHERE media_id = ? AND date_publication >= ?
            """, (media_id, date_limit))
            
            fb_row = cursor.fetchone()
            
            metrics = {
                'media_id': media_id,
                'periode_debut': periode_debut,
                'periode_fin': periode_fin,
                'total_articles': total_articles,
                'total_posts_facebook': fb_row['total_posts'] or 0,
                'total_likes': fb_row['total_likes'] or 0,
                'total_comments': fb_row['total_comments'] or 0,
                'total_shares': fb_row['total_shares'] or 0,
                'engagement_total': fb_row['engagement_total'] or 0,
                'engagement_moyen': fb_row['engagement_moyen'] or 0
            }
            
            # Sauvegarder les métriques
            cursor.execute("""
                INSERT INTO media_metrics (
                    media_id, periode_debut, periode_fin,
                    total_articles, total_posts_facebook,
                    total_likes, total_comments, total_shares,
                    engagement_total, engagement_moyen
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                media_id, periode_debut, periode_fin,
                metrics['total_articles'], metrics['total_posts_facebook'],
                metrics['total_likes'], metrics['total_comments'], metrics['total_shares'],
                metrics['engagement_total'], metrics['engagement_moyen']
            ))
            
            conn.commit()
            
            return metrics
        
        finally:
            conn.close()
    
    def get_media_ranking(self, days: int = 30) -> List[Dict[str, Any]]:
        """Classement des médias par engagement"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            date_limit = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute("""
                SELECT 
                    m.id,
                    m.nom,
                    m.url,
                    COUNT(DISTINCT a.id) as total_articles,
                    COUNT(DISTINCT fp.id) as total_posts_facebook,
                    COALESCE(SUM(fp.likes), 0) as total_likes,
                    COALESCE(SUM(fp.comments), 0) as total_comments,
                    COALESCE(SUM(fp.shares), 0) as total_shares,
                    COALESCE(SUM(fp.engagement_total), 0) as engagement_total,
                    COALESCE(AVG(fp.engagement_total), 0) as engagement_moyen
                FROM medias m
                LEFT JOIN articles a ON m.id = a.media_id AND a.date_publication >= ?
                LEFT JOIN facebook_posts fp ON m.id = fp.media_id AND fp.date_publication >= ?
                WHERE m.actif = 1
                GROUP BY m.id, m.nom, m.url
                ORDER BY engagement_total DESC, total_articles DESC
            """, (date_limit, date_limit))
            
            return [dict(row) for row in cursor.fetchall()]
        
        finally:
            conn.close()
    
    # ==================== TWITTER ====================
    
    def add_twitter_tweet(self, media_id: int, tweet_id: str, text: str,
                         url: str, image_url: str = None, date_publication: str = None,
                         retweets: int = 0, replies: int = 0, likes: int = 0,
                         quotes: int = 0, impressions: int = 0) -> int:
        """Ajoute ou met à jour un tweet"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        engagement_total = retweets + replies + likes + quotes
        
        try:
            cursor.execute("""
                INSERT INTO twitter_tweets (
                    media_id, tweet_id, text, url, image_url, date_publication,
                    retweets, replies, likes, quotes, impressions, engagement_total
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(tweet_id) DO UPDATE SET
                    retweets = excluded.retweets,
                    replies = excluded.replies,
                    likes = excluded.likes,
                    quotes = excluded.quotes,
                    impressions = excluded.impressions,
                    engagement_total = excluded.engagement_total,
                    scraped_at = CURRENT_TIMESTAMP
            """, (
                media_id, tweet_id, text, url, image_url, date_publication,
                retweets, replies, likes, quotes, impressions, engagement_total
            ))
            
            tweet_id_db = cursor.lastrowid
            conn.commit()
            
            return tweet_id_db
        
        finally:
            conn.close()
    
    def get_twitter_tweets_by_media(self, media_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupère les tweets d'un média"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM twitter_tweets
                WHERE media_id = ?
                ORDER BY date_publication DESC
                LIMIT ?
            """, (media_id, limit))
            
            return [dict(row) for row in cursor.fetchall()]
        
        finally:
            conn.close()
    
    def calculate_media_metrics_with_twitter(self, media_id: int, days: int = 30) -> Optional[Dict[str, Any]]:
        """Calcule les métriques d'un média (articles + Facebook + Twitter)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            date_limit = (datetime.now() - timedelta(days=days)).isoformat()
            periode_debut = date_limit
            periode_fin = datetime.now().isoformat()
            
            # Compter les articles
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM articles
                WHERE media_id = ? AND date_publication >= ?
            """, (media_id, date_limit))
            
            total_articles = cursor.fetchone()['total']
            
            # Métriques Facebook
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_posts,
                    SUM(likes) as total_likes,
                    SUM(comments) as total_comments,
                    SUM(shares) as total_shares,
                    SUM(engagement_total) as engagement_total
                FROM facebook_posts
                WHERE media_id = ? AND date_publication >= ?
            """, (media_id, date_limit))
            
            fb_row = cursor.fetchone()
            
            # Métriques Twitter
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_tweets,
                    SUM(retweets) as total_retweets,
                    SUM(replies) as total_replies,
                    SUM(likes) as total_likes,
                    SUM(quotes) as total_quotes,
                    SUM(impressions) as total_impressions,
                    SUM(engagement_total) as engagement_total
                FROM twitter_tweets
                WHERE media_id = ? AND date_publication >= ?
            """, (media_id, date_limit))
            
            tw_row = cursor.fetchone()
            
            # Calculer l'engagement total
            engagement_fb = fb_row['engagement_total'] or 0
            engagement_tw = tw_row['engagement_total'] or 0
            engagement_total = engagement_fb + engagement_tw
            
            total_posts = (fb_row['total_posts'] or 0) + (tw_row['total_tweets'] or 0)
            engagement_moyen = engagement_total / total_posts if total_posts > 0 else 0
            
            metrics = {
                'media_id': media_id,
                'periode_debut': periode_debut,
                'periode_fin': periode_fin,
                'total_articles': total_articles,
                'total_posts_facebook': fb_row['total_posts'] or 0,
                'total_tweets': tw_row['total_tweets'] or 0,
                'total_likes_fb': fb_row['total_likes'] or 0,
                'total_comments_fb': fb_row['total_comments'] or 0,
                'total_shares_fb': fb_row['total_shares'] or 0,
                'engagement_total_fb': engagement_fb,
                'total_retweets': tw_row['total_retweets'] or 0,
                'total_replies': tw_row['total_replies'] or 0,
                'total_likes_tw': tw_row['total_likes'] or 0,
                'total_quotes': tw_row['total_quotes'] or 0,
                'total_impressions': tw_row['total_impressions'] or 0,
                'engagement_total_tw': engagement_tw,
                'engagement_total': engagement_total,
                'engagement_moyen': engagement_moyen
            }
            
            # Sauvegarder les métriques
            cursor.execute("""
                INSERT INTO media_metrics (
                    media_id, periode_debut, periode_fin,
                    total_articles, total_posts_facebook, total_tweets,
                    total_likes_fb, total_comments_fb, total_shares_fb, engagement_total_fb,
                    total_retweets, total_replies, total_likes_tw, total_quotes,
                    total_impressions, engagement_total_tw,
                    engagement_total, engagement_moyen
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                media_id, periode_debut, periode_fin,
                metrics['total_articles'], metrics['total_posts_facebook'], metrics['total_tweets'],
                metrics['total_likes_fb'], metrics['total_comments_fb'], metrics['total_shares_fb'],
                metrics['engagement_total_fb'],
                metrics['total_retweets'], metrics['total_replies'], metrics['total_likes_tw'],
                metrics['total_quotes'], metrics['total_impressions'], metrics['engagement_total_tw'],
                metrics['engagement_total'], metrics['engagement_moyen']
            ))
            
            conn.commit()
            
            return metrics
        
        finally:
            conn.close()
    
    def get_media_ranking_with_twitter(self, days: int = 30) -> List[Dict[str, Any]]:
        """Classement des médias par engagement (Facebook + Twitter)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            date_limit = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute("""
                SELECT 
                    m.id,
                    m.nom,
                    m.url,
                    COUNT(DISTINCT a.id) as total_articles,
                    COUNT(DISTINCT fp.id) as total_posts_facebook,
                    COUNT(DISTINCT tw.id) as total_tweets,
                    COALESCE(SUM(fp.likes), 0) as total_likes_fb,
                    COALESCE(SUM(fp.comments), 0) as total_comments_fb,
                    COALESCE(SUM(fp.shares), 0) as total_shares_fb,
                    COALESCE(SUM(fp.engagement_total), 0) as engagement_total_fb,
                    COALESCE(SUM(tw.retweets), 0) as total_retweets,
                    COALESCE(SUM(tw.replies), 0) as total_replies,
                    COALESCE(SUM(tw.likes), 0) as total_likes_tw,
                    COALESCE(SUM(tw.quotes), 0) as total_quotes,
                    COALESCE(SUM(tw.impressions), 0) as total_impressions,
                    COALESCE(SUM(tw.engagement_total), 0) as engagement_total_tw,
                    COALESCE(SUM(fp.engagement_total), 0) + COALESCE(SUM(tw.engagement_total), 0) as engagement_total,
                    CASE 
                        WHEN (COUNT(DISTINCT fp.id) + COUNT(DISTINCT tw.id)) > 0 
                        THEN (COALESCE(SUM(fp.engagement_total), 0) + COALESCE(SUM(tw.engagement_total), 0)) / 
                             (COUNT(DISTINCT fp.id) + COUNT(DISTINCT tw.id))
                        ELSE 0 
                    END as engagement_moyen
                FROM medias m
                LEFT JOIN articles a ON m.id = a.media_id AND a.date_publication >= ?
                LEFT JOIN facebook_posts fp ON m.id = fp.media_id AND fp.date_publication >= ?
                LEFT JOIN twitter_tweets tw ON m.id = tw.media_id AND tw.date_publication >= ?
                WHERE m.actif = 1
                GROUP BY m.id, m.nom, m.url
                ORDER BY engagement_total DESC, total_articles DESC
            """, (date_limit, date_limit, date_limit))
            
            return [dict(row) for row in cursor.fetchall()]
        
        finally:
            conn.close()
    
    # ==================== CONTENT MODERATION ====================
    
    def add_content_moderation(self, content_type: str, content_id: int, analysis: dict) -> int:
        """
        Ajoute ou met à jour une analyse de modération
        
        Args:
            content_type: Type de contenu ('article', 'facebook_post', 'tweet')
            content_id: ID du contenu
            analysis: Résultat de l'analyse
            
        Returns:
            ID de l'analyse
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            import json
            
            toxicity = analysis.get('toxicity', {})
            misinformation = analysis.get('misinformation', {})
            sensitivity = analysis.get('sensitivity', {})
            
            cursor.execute("""
                INSERT OR REPLACE INTO content_moderation (
                    content_type, content_id,
                    risk_score, risk_level, should_flag,
                    is_toxic, toxicity_score, hate_speech_score, violence_score, 
                    insults_score, discrimination_score, toxicity_reason,
                    is_misinformation, misinformation_score, unverified_claims_score,
                    fact_manipulation_score, conspiracy_score, propaganda_score,
                    suspicious_elements, misinformation_reason,
                    is_sensitive, sensitivity_level, sensitivity_score,
                    sensitive_categories, sensitivity_reason,
                    analyzed_at, model_used
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                content_type, content_id,
                analysis.get('risk_score', 0),
                analysis.get('risk_level', 'MINIMAL'),
                1 if analysis.get('should_flag', False) else 0,
                1 if toxicity.get('est_toxique', False) else 0,
                toxicity.get('score_toxicite', 0),
                toxicity.get('incitation_haine', 0),
                toxicity.get('violence', 0),
                toxicity.get('insultes', 0),
                toxicity.get('discrimination', 0),
                toxicity.get('raison', ''),
                1 if misinformation.get('est_desinformation', False) else 0,
                misinformation.get('score_desinformation', 0),
                misinformation.get('affirmations_non_verifiees', 0),
                misinformation.get('manipulation_faits', 0),
                misinformation.get('theorie_complot', 0),
                misinformation.get('propagande', 0),
                json.dumps(misinformation.get('elements_suspects', [])),
                misinformation.get('raison', ''),
                1 if sensitivity.get('est_sensible', False) else 0,
                sensitivity.get('niveau_sensibilite', 'faible'),
                sensitivity.get('score_sensibilite', 0),
                json.dumps(sensitivity.get('categories_sensibles', [])),
                sensitivity.get('raison', ''),
                analysis.get('analyzed_at'),
                'llama3.2'
            ))
            
            conn.commit()
            return cursor.lastrowid
            
        finally:
            conn.close()
    
    def get_content_moderation(self, content_type: str, content_id: int) -> Optional[dict]:
        """
        Récupère l'analyse de modération d'un contenu
        
        Args:
            content_type: Type de contenu
            content_id: ID du contenu
            
        Returns:
            Dict avec l'analyse ou None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM content_moderation
                WHERE content_type = ? AND content_id = ?
            """, (content_type, content_id))
            
            row = cursor.fetchone()
            if row:
                import json
                return {
                    'id': row['id'],
                    'content_type': row['content_type'],
                    'content_id': row['content_id'],
                    'risk_score': row['risk_score'],
                    'risk_level': row['risk_level'],
                    'should_flag': bool(row['should_flag']),
                    'is_toxic': bool(row['is_toxic']),
                    'toxicity_score': row['toxicity_score'],
                    'is_misinformation': bool(row['is_misinformation']),
                    'misinformation_score': row['misinformation_score'],
                    'is_sensitive': bool(row['is_sensitive']),
                    'sensitivity_score': row['sensitivity_score'],
                    'analyzed_at': row['analyzed_at']
                }
            return None
            
        finally:
            conn.close()
    
    def get_flagged_contents(self, content_type: Optional[str] = None, limit: int = 100) -> List[dict]:
        """
        Récupère les contenus signalés
        
        Args:
            content_type: Type de contenu à filtrer (optionnel)
            limit: Nombre maximum de résultats
            
        Returns:
            Liste des contenus signalés
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if content_type:
                cursor.execute("""
                    SELECT * FROM content_moderation
                    WHERE should_flag = 1 AND content_type = ?
                    ORDER BY risk_score DESC
                    LIMIT ?
                """, (content_type, limit))
            else:
                cursor.execute("""
                    SELECT * FROM content_moderation
                    WHERE should_flag = 1
                    ORDER BY risk_score DESC
                    LIMIT ?
                """, (limit,))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row['id'],
                    'content_type': row['content_type'],
                    'content_id': row['content_id'],
                    'risk_score': row['risk_score'],
                    'risk_level': row['risk_level'],
                    'is_toxic': bool(row['is_toxic']),
                    'is_misinformation': bool(row['is_misinformation']),
                    'is_sensitive': bool(row['is_sensitive']),
                    'analyzed_at': row['analyzed_at']
                })
            
            return results
            
        finally:
            conn.close()
    
    def get_moderation_stats(self) -> dict:
        """
        Récupère les statistiques de modération
        
        Returns:
            Dict avec les statistiques
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_analyzed,
                    SUM(CASE WHEN should_flag = 1 THEN 1 ELSE 0 END) as total_flagged,
                    SUM(CASE WHEN is_toxic = 1 THEN 1 ELSE 0 END) as total_toxic,
                    SUM(CASE WHEN is_misinformation = 1 THEN 1 ELSE 0 END) as total_misinfo,
                    SUM(CASE WHEN is_sensitive = 1 THEN 1 ELSE 0 END) as total_sensitive,
                    AVG(risk_score) as avg_risk_score
                FROM content_moderation
            """)
            
            row = cursor.fetchone()
            return {
                'total_analyzed': row['total_analyzed'] or 0,
                'total_flagged': row['total_flagged'] or 0,
                'total_toxic': row['total_toxic'] or 0,
                'total_misinformation': row['total_misinfo'] or 0,
                'total_sensitive': row['total_sensitive'] or 0,
                'avg_risk_score': round(row['avg_risk_score'] or 0, 2)
            }
            
        finally:
            conn.close()
    
    # ==================== UTILITAIRES ====================
    
    def vacuum(self):
        """Optimise la base de données"""
        conn = self.get_connection()
        try:
            conn.execute("VACUUM")
            conn.commit()
        finally:
            conn.close()
