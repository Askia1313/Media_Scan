"""
Gestionnaire de base de données SQLite
"""

import sqlite3
import json
import os
from datetime import datetime
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
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtenir une connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
        return conn
    
    def init_database(self):
        """Initialiser la base de données avec le schéma"""
        schema_path = Path(__file__).parent / 'schema.sql'
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()
        
        conn = self.get_connection()
        conn.executescript(schema)
        conn.commit()
        conn.close()
        
        print("✅ Base de données initialisée")
    
    # === GESTION DES MÉDIAS ===
    
    def add_media(self, nom: str, url: str, type_site: str = 'unknown') -> int:
        """
        Ajouter un média
        
        Args:
            nom: Nom du média
            url: URL du site
            type_site: Type de site (wordpress, html, autre)
        
        Returns:
            ID du média créé ou existant
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
    
    def update_media_last_scrape(self, media_id: int):
        """Mettre à jour la date de dernière collecte d'un média"""
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
    
    def get_all_active_medias(self) -> List[Media]:
        """Récupérer tous les médias actifs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM medias WHERE actif = 1 ORDER BY nom")
            rows = cursor.fetchall()
            
            return [
                Media(
                    id=row['id'],
                    nom=row['nom'],
                    url=row['url'],
                    type_site=row['type_site'],
                    actif=bool(row['actif']),
                    derniere_collecte=row['derniere_collecte'],
                    created_at=row['created_at']
                )
                for row in rows
            ]
        
        finally:
            conn.close()
    
    # === GESTION DES ARTICLES ===
    
    def add_article(self, article: Article) -> Optional[int]:
        """
        Ajouter un article
        
        Args:
            article: Instance d'Article
        
        Returns:
            ID de l'article créé, ou None si déjà existant
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Convertir les listes en JSON si nécessaire
            categories_json = json.dumps(article.categories) if isinstance(article.categories, list) else article.categories
            tags_json = json.dumps(article.tags) if isinstance(article.tags, list) else article.tags
            
            cursor.execute("""
                INSERT OR IGNORE INTO articles 
                (media_id, titre, contenu, extrait, url, auteur, date_publication,
                 image_url, categories, tags, source_type, vues, commentaires)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article.media_id,
                article.titre,
                article.contenu,
                article.extrait,
                article.url,
                article.auteur,
                article.date_publication,
                article.image_url,
                categories_json,
                tags_json,
                article.source_type,
                article.vues,
                article.commentaires
            ))
            
            article_id = cursor.lastrowid
            conn.commit()
            
            # Retourner None si l'article existait déjà (IGNORE)
            return article_id if article_id > 0 else None
        
        finally:
            conn.close()
    
    def article_exists(self, url: str) -> bool:
        """Vérifier si un article existe déjà"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) as count FROM articles WHERE url = ?", (url,))
            count = cursor.fetchone()['count']
            return count > 0
        
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
            
            rows = cursor.fetchall()
            return [self._row_to_article(row) for row in rows]
        
        finally:
            conn.close()
    
    def get_recent_articles(self, days: int = 30, limit: int = 100) -> List[Article]:
        """Récupérer les articles récents"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM articles 
                WHERE date_publication >= datetime('now', '-' || ? || ' days')
                ORDER BY date_publication DESC
                LIMIT ?
            """, (days, limit))
            
            rows = cursor.fetchall()
            return [self._row_to_article(row) for row in rows]
        
        finally:
            conn.close()
    
    def get_article_count(self, media_id: Optional[int] = None) -> int:
        """Compter les articles (total ou par média)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if media_id:
                cursor.execute("SELECT COUNT(*) as count FROM articles WHERE media_id = ?", (media_id,))
            else:
                cursor.execute("SELECT COUNT(*) as count FROM articles")
            
            return cursor.fetchone()['count']
        
        finally:
            conn.close()
    
    def _row_to_article(self, row: sqlite3.Row) -> Article:
        """Convertir une ligne SQL en objet Article"""
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
            categories=row['categories'],
            tags=row['tags'],
            source_type=row['source_type'],
            scraped_at=row['scraped_at'],
            vues=row['vues'],
            commentaires=row['commentaires'],
            created_at=row['created_at']
        )
    
    # === LOGS DE SCRAPING ===
    
    def add_scraping_log(self, media_id: int, status: str, methode: str, 
                        articles_collectes: int = 0, message: str = ""):
        """Ajouter un log de scraping"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO scraping_logs 
                (media_id, status, methode, articles_collectes, message)
                VALUES (?, ?, ?, ?, ?)
            """, (media_id, status, methode, articles_collectes, message))
            
            conn.commit()
        
        finally:
            conn.close()
    
    def get_scraping_stats(self) -> Dict[str, Any]:
        """Obtenir des statistiques de scraping"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Total articles
            cursor.execute("SELECT COUNT(*) as total FROM articles")
            total_articles = cursor.fetchone()['total']
            
            # Articles par média
            cursor.execute("""
                SELECT m.nom, COUNT(a.id) as count
                FROM medias m
                LEFT JOIN articles a ON m.id = a.media_id
                GROUP BY m.id
                ORDER BY count DESC
            """)
            articles_par_media = dict(cursor.fetchall())
            
            # Articles par source
            cursor.execute("""
                SELECT source_type, COUNT(*) as count
                FROM articles
                GROUP BY source_type
            """)
            articles_par_source = dict(cursor.fetchall())
            
            # Derniers logs
            cursor.execute("""
                SELECT l.*, m.nom as media_nom
                FROM scraping_logs l
                JOIN medias m ON l.media_id = m.id
                ORDER BY l.created_at DESC
                LIMIT 10
            """)
            derniers_logs = [dict(row) for row in cursor.fetchall()]
            
            return {
                'total_articles': total_articles,
                'articles_par_media': articles_par_media,
                'articles_par_source': articles_par_source,
                'derniers_logs': derniers_logs
            }
        
        finally:
            conn.close()
    
    # === UTILITAIRES ===
    
    def clear_old_articles(self, days: int = 90):
        """Supprimer les articles de plus de X jours"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                DELETE FROM articles 
                WHERE date_publication < datetime('now', '-' || ? || ' days')
            """, (days,))
            
            deleted = cursor.rowcount
            conn.commit()
            
            print(f"🗑️ {deleted} articles supprimés (> {days} jours)")
            return deleted
        
        finally:
            conn.close()
    
    def vacuum(self):
        """Optimiser la base de données"""
        conn = self.get_connection()
        conn.execute("VACUUM")
        conn.close()
        print("✅ Base de données optimisée")
