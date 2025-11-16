"""
Analyseur d'audience multi-plateformes
Analyse séparée : Web, Facebook, Twitter
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
from database.db_manager import DatabaseManager


class AudienceAnalyzer:
    """Analyseur d'audience par plateforme"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    # ==================== AUDIENCE WEB ====================
    
    def analyze_web_audience(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Analyse de l'audience Web (articles)
        
        Returns:
            Liste des médias avec métriques web
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            date_limit = (datetime.now() - timedelta(days=days)).isoformat()
            now = datetime.now().isoformat()
            
            cursor.execute("""
                SELECT 
                    m.id,
                    m.nom,
                    m.url,
                    COUNT(a.id) as total_articles,
                    MAX(a.date_publication) as derniere_publication,
                    MIN(a.date_publication) as premiere_publication,
                    COUNT(DISTINCT DATE(a.date_publication)) as jours_avec_publication,
                    CASE 
                        WHEN MAX(a.date_publication) IS NULL THEN 999
                        ELSE CAST((julianday(?) - julianday(MAX(a.date_publication))) AS INTEGER)
                    END as jours_depuis_derniere_pub
                FROM medias m
                LEFT JOIN articles a ON m.id = a.media_id 
                    AND a.date_publication >= ?
                WHERE m.actif = 1
                GROUP BY m.id, m.nom, m.url
                ORDER BY total_articles DESC
            """, (now, date_limit))
            
            results = []
            for row in cursor.fetchall():
                # Calculer la moyenne quotidienne réelle
                jours_avec_pub = row['jours_avec_publication'] or 0
                total_articles = row['total_articles']
                
                if jours_avec_pub > 0:
                    articles_par_jour_moyen = round(total_articles / jours_avec_pub, 2)
                else:
                    articles_par_jour_moyen = 0
                
                results.append({
                    'id': row['id'],
                    'nom': row['nom'],
                    'url': row['url'],
                    'total_articles': total_articles,
                    'derniere_publication': row['derniere_publication'],
                    'premiere_publication': row['premiere_publication'],
                    'jours_avec_publication': jours_avec_pub,
                    'articles_par_jour_moyen': articles_par_jour_moyen,
                    'jours_depuis_derniere_pub': row['jours_depuis_derniere_pub'],
                    'statut': self._get_publication_status(row['jours_depuis_derniere_pub'])
                })
            
            return results
        
        finally:
            conn.close()
    
    # ==================== AUDIENCE FACEBOOK ====================
    
    def analyze_facebook_audience(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Analyse de l'audience Facebook
        
        Returns:
            Liste des médias avec métriques Facebook
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            date_limit = (datetime.now() - timedelta(days=days)).isoformat()
            now = datetime.now().isoformat()
            
            cursor.execute("""
                SELECT 
                    m.id,
                    m.nom,
                    m.url,
                    m.facebook_page,
                    COUNT(fp.id) as total_posts,
                    SUM(fp.likes) as total_likes,
                    SUM(fp.comments) as total_comments,
                    SUM(fp.shares) as total_shares,
                    SUM(fp.engagement_total) as engagement_total,
                    ROUND(AVG(fp.engagement_total), 2) as engagement_moyen,
                    MAX(fp.date_publication) as derniere_publication,
                    COUNT(DISTINCT DATE(fp.date_publication)) as jours_avec_publication,
                    CASE 
                        WHEN MAX(fp.date_publication) IS NULL THEN 999
                        ELSE CAST((julianday(?) - julianday(MAX(fp.date_publication))) AS INTEGER)
                    END as jours_depuis_derniere_pub
                FROM medias m
                LEFT JOIN facebook_posts fp ON m.id = fp.media_id 
                    AND fp.date_publication >= ?
                WHERE m.actif = 1 AND m.facebook_page IS NOT NULL
                GROUP BY m.id, m.nom, m.url, m.facebook_page
                ORDER BY engagement_total DESC
            """, (now, date_limit))
            
            results = []
            for row in cursor.fetchall():
                # Calculer la moyenne quotidienne réelle
                jours_avec_pub = row['jours_avec_publication'] or 0
                total_posts = row['total_posts'] or 0
                
                if jours_avec_pub > 0:
                    posts_par_jour_moyen = round(total_posts / jours_avec_pub, 2)
                else:
                    posts_par_jour_moyen = 0
                
                results.append({
                    'id': row['id'],
                    'nom': row['nom'],
                    'url': row['url'],
                    'facebook_page': row['facebook_page'],
                    'total_posts': total_posts,
                    'total_likes': row['total_likes'] or 0,
                    'total_comments': row['total_comments'] or 0,
                    'total_shares': row['total_shares'] or 0,
                    'engagement_total': row['engagement_total'] or 0,
                    'engagement_moyen': row['engagement_moyen'] or 0,
                    'derniere_publication': row['derniere_publication'],
                    'jours_avec_publication': jours_avec_pub,
                    'posts_par_jour_moyen': posts_par_jour_moyen,
                    'jours_depuis_derniere_pub': row['jours_depuis_derniere_pub'],
                    'statut': self._get_publication_status(row['jours_depuis_derniere_pub'])
                })
            
            return results
        
        finally:
            conn.close()
    
    # ==================== AUDIENCE TWITTER ====================
    
    def analyze_twitter_audience(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Analyse de l'audience Twitter
        
        Returns:
            Liste des médias avec métriques Twitter
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            date_limit = (datetime.now() - timedelta(days=days)).isoformat()
            now = datetime.now().isoformat()
            
            cursor.execute("""
                SELECT 
                    m.id,
                    m.nom,
                    m.url,
                    m.twitter_account,
                    COUNT(tw.id) as total_tweets,
                    SUM(tw.retweets) as total_retweets,
                    SUM(tw.replies) as total_replies,
                    SUM(tw.likes) as total_likes,
                    SUM(tw.quotes) as total_quotes,
                    SUM(tw.impressions) as total_impressions,
                    SUM(tw.engagement_total) as engagement_total,
                    ROUND(AVG(tw.engagement_total), 2) as engagement_moyen,
                    MAX(tw.date_publication) as derniere_publication,
                    COUNT(DISTINCT DATE(tw.date_publication)) as jours_avec_publication,
                    CASE 
                        WHEN MAX(tw.date_publication) IS NULL THEN 999
                        ELSE CAST((julianday(?) - julianday(MAX(tw.date_publication))) AS INTEGER)
                    END as jours_depuis_derniere_pub
                FROM medias m
                LEFT JOIN twitter_tweets tw ON m.id = tw.media_id 
                    AND tw.date_publication >= ?
                WHERE m.actif = 1 AND m.twitter_account IS NOT NULL
                GROUP BY m.id, m.nom, m.url, m.twitter_account
                ORDER BY engagement_total DESC
            """, (now, date_limit))
            
            results = []
            for row in cursor.fetchall():
                # Calculer la moyenne quotidienne réelle
                jours_avec_pub = row['jours_avec_publication'] or 0
                total_tweets = row['total_tweets'] or 0
                
                if jours_avec_pub > 0:
                    tweets_par_jour_moyen = round(total_tweets / jours_avec_pub, 2)
                else:
                    tweets_par_jour_moyen = 0
                
                results.append({
                    'id': row['id'],
                    'nom': row['nom'],
                    'url': row['url'],
                    'twitter_account': row['twitter_account'],
                    'total_tweets': total_tweets,
                    'total_retweets': row['total_retweets'] or 0,
                    'total_replies': row['total_replies'] or 0,
                    'total_likes': row['total_likes'] or 0,
                    'total_quotes': row['total_quotes'] or 0,
                    'total_impressions': row['total_impressions'] or 0,
                    'engagement_total': row['engagement_total'] or 0,
                    'engagement_moyen': row['engagement_moyen'] or 0,
                    'derniere_publication': row['derniere_publication'],
                    'jours_avec_publication': jours_avec_pub,
                    'tweets_par_jour_moyen': tweets_par_jour_moyen,
                    'jours_depuis_derniere_pub': row['jours_depuis_derniere_pub'],
                    'statut': self._get_publication_status(row['jours_depuis_derniere_pub'])
                })
            
            return results
        
        finally:
            conn.close()
    
    # ==================== ANALYSE GLOBALE ====================
    
    def analyze_global_audience(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Analyse globale combinant toutes les plateformes
        
        Returns:
            Liste des médias avec métriques combinées
        """
        web_data = {m['id']: m for m in self.analyze_web_audience(days)}
        fb_data = {m['id']: m for m in self.analyze_facebook_audience(days)}
        tw_data = {m['id']: m for m in self.analyze_twitter_audience(days)}
        
        # Combiner les données
        all_media_ids = set(web_data.keys()) | set(fb_data.keys()) | set(tw_data.keys())
        
        results = []
        for media_id in all_media_ids:
            web = web_data.get(media_id, {})
            fb = fb_data.get(media_id, {})
            tw = tw_data.get(media_id, {})
            
            # Calculer le score d'influence composite
            total_publications = (
                web.get('total_articles', 0) +
                fb.get('total_posts', 0) +
                tw.get('total_tweets', 0)
            )
            
            total_engagement = (
                fb.get('engagement_total', 0) +
                tw.get('engagement_total', 0)
            )
            
            # Score composite (40% volume, 60% engagement)
            score_volume = total_publications / 10  # Normaliser
            score_engagement = total_engagement / 100  # Normaliser
            score_influence = (0.4 * score_volume) + (0.6 * score_engagement)
            
            results.append({
                'id': media_id,
                'nom': web.get('nom') or fb.get('nom') or tw.get('nom'),
                'url': web.get('url') or fb.get('url') or tw.get('url'),
                'total_publications': total_publications,
                'total_engagement': total_engagement,
                'score_influence': round(score_influence, 2),
                'web': web,
                'facebook': fb,
                'twitter': tw
            })
        
        # Trier par score d'influence
        results.sort(key=lambda x: x['score_influence'], reverse=True)
        
        return results
    
    # ==================== UTILITAIRES ====================
    
    def _get_publication_status(self, jours: int) -> str:
        """Détermine le statut de publication"""
        if jours == 999:
            return "❌ Aucune publication"
        elif jours == 0:
            return "🟢 Actif (aujourd'hui)"
        elif jours <= 1:
            return "🟢 Actif (hier)"
        elif jours <= 3:
            return "🟡 Récent (3 jours)"
        elif jours <= 7:
            return "🟡 Récent (1 semaine)"
        elif jours <= 14:
            return "🟠 Modéré (2 semaines)"
        elif jours <= 30:
            return "🟠 Modéré (1 mois)"
        else:
            return f"🔴 Inactif ({jours} jours)"
    
    def get_inactive_medias(self, days_threshold: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """
        Récupère les médias inactifs par plateforme
        
        Args:
            days_threshold: Nombre de jours sans publication pour être considéré inactif
            
        Returns:
            Dictionnaire avec médias inactifs par plateforme
        """
        web = [m for m in self.analyze_web_audience() 
               if m['jours_depuis_derniere_pub'] > days_threshold]
        
        facebook = [m for m in self.analyze_facebook_audience() 
                   if m['jours_depuis_derniere_pub'] > days_threshold]
        
        twitter = [m for m in self.analyze_twitter_audience() 
                  if m['jours_depuis_derniere_pub'] > days_threshold]
        
        return {
            'web': web,
            'facebook': facebook,
            'twitter': twitter
        }
