"""
Gestionnaire principal de scraping avec fallback automatique
Priorité: RSS > HTML Scraping
Classification automatique après scraping
"""

from typing import List, Tuple
from urllib.parse import urlparse

from database.db_manager import DatabaseManager
from database.models import Article
from .rss_scraper import RSScraper
from .smart_html_scraper import SmartHTMLScraper
from analysis.theme_classifier import ThemeClassifier


class ScraperManager:
    """Gestionnaire de scraping intelligent avec RSS et HTML"""
    
    def __init__(self, db_manager: DatabaseManager, auto_classify: bool = True):
        """
        Initialise le gestionnaire
        
        Args:
            db_manager: Instance de DatabaseManager
            auto_classify: Activer la classification automatique après scraping
        """
        self.db = db_manager
        self.auto_classify = auto_classify
        self.classifier = None
        
        # Initialiser le classificateur si activé
        if self.auto_classify:
            try:
                self.classifier = ThemeClassifier()
                # Vérifier si Ollama est accessible
                if not self.classifier.check_ollama_status():
                    print("⚠️ Ollama non accessible, classification désactivée")
                    self.auto_classify = False
            except Exception as e:
                print(f"⚠️ Erreur initialisation classificateur: {e}")
                self.auto_classify = False
    
    def scrape_site(self, url: str, days: int = 30) -> Tuple[int, str, str]:
        """
        Scraper un site avec RSS en priorité, sinon HTML
        
        Args:
            url: URL du site à scraper
            days: Nombre de jours à récupérer
        
        Returns:
            Tuple (nombre d'articles, méthode utilisée, message)
        """
        # Nettoyer l'URL
        url = url.strip().rstrip('/')
        
        # Extraire le nom du domaine pour le nom du média
        domain = urlparse(url).netloc
        media_name = domain.replace('www.', '').split('.')[0].capitalize()
        
        print(f"\n{'='*60}")
        print(f"🎯 Scraping: {media_name} ({url})")
        print(f"{'='*60}\n")
        
        try:
            # Essayer d'abord avec RSS
            print(f"🔄 Tentative 1/2: Scraping RSS...")
            rss_scraper = RSScraper(url)
            articles = rss_scraper.scrape(media_id=0, days=days)  # media_id temporaire
            
            # Si RSS a fonctionné
            if len(articles) > 0:
                # Ajouter ou récupérer le média
                media_id = self.db.add_media(media_name, url)
                
                # Mettre à jour les media_id
                for article in articles:
                    article.media_id = media_id
                
                # Sauvegarder
                saved_count, new_article_ids = self._save_articles(articles)
                
                # Classification automatique des nouveaux articles
                if self.auto_classify and new_article_ids:
                    self._classify_articles(new_article_ids)
                
                # Mettre à jour la date de dernière collecte
                self.db.update_media_last_scrape(media_id)
                
                # Logger
                self.db.add_scraping_log(
                    media_id=media_id,
                    status='success',
                    methode='rss_feed',
                    articles_collectes=saved_count,
                    message=f"{saved_count} articles collectés via RSS"
                )
                
                return saved_count, 'rss_feed', f"✅ {saved_count} articles collectés via RSS"
            
            # Si RSS n'a pas fonctionné, fallback vers HTML
            print(f"\n🔄 Tentative 2/2: Scraping HTML...")
            scraper = SmartHTMLScraper(url)
            
            # Ajouter/mettre à jour le média
            media_id = self.db.add_media(media_name, url, 'html')
            
            # Scraper les articles
            articles = scraper.scrape(media_id, days=days, max_articles=100)
            
            # Sauvegarder en base
            saved_count, new_article_ids = self._save_articles(articles)
            
            # Classification automatique des nouveaux articles
            if self.auto_classify and new_article_ids:
                self._classify_articles(new_article_ids)
            
            # Mettre à jour la date de dernière collecte
            self.db.update_media_last_scrape(media_id)
            
            # Logger
            self.db.add_scraping_log(
                media_id=media_id,
                status='success' if saved_count > 0 else 'partial',
                methode='html_scraping',
                articles_collectes=saved_count,
                message=f"{saved_count} articles collectés via scraping HTML"
            )
            
            return saved_count, 'html_scraping', f"✅ {saved_count} articles collectés via scraping HTML"
        
        except Exception as e:
            error_msg = f"❌ Erreur scraping: {e}"
            print(error_msg)
            
            # Logger l'erreur
            media_id = self.db.add_media(media_name, url, 'unknown')
            self.db.add_scraping_log(
                media_id=media_id,
                status='error',
                methode='html_scraping',
                articles_collectes=0,
                message=str(e)
            )
            
            return 0, 'error', error_msg
    
    def _save_articles(self, articles: List[Article]) -> Tuple[int, List[int]]:
        """
        Sauvegarder les articles en base de données
        
        Args:
            articles: Liste d'articles à sauvegarder
        
        Returns:
            Tuple (nombre d'articles sauvegardés, liste des IDs des nouveaux articles)
        """
        saved_count = 0
        duplicate_count = 0
        new_article_ids = []
        
        for article in articles:
            # Vérifier si l'article existe déjà
            if not self.db.article_exists(article.url):
                article_id = self.db.add_article(article)
                if article_id:
                    saved_count += 1
                    new_article_ids.append(article_id)
            else:
                duplicate_count += 1
        
        if duplicate_count > 0:
            print(f"   💾 {saved_count} nouveaux articles, {duplicate_count} doublons ignorés")
        
        return saved_count, new_article_ids
    
    def _classify_articles(self, article_ids: List[int]):
        """
        Classifier automatiquement les articles
        
        Args:
            article_ids: Liste des IDs d'articles à classifier
        """
        if not self.classifier or not article_ids:
            return
        
        print(f"\n🤖 Classification automatique de {len(article_ids)} articles...")
        
        classified_count = 0
        errors = 0
        
        for article_id in article_ids:
            try:
                # Récupérer l'article
                article = self.db.get_article(article_id)
                if not article:
                    continue
                
                # Classifier
                result = self.classifier.classify_article(
                    article.get('titre', ''),
                    article.get('contenu', '')
                )
                
                # Sauvegarder la classification
                self.db.add_classification(
                    article_id=article_id,
                    categorie=result['categorie'],
                    confiance=result['confiance'],
                    mots_cles=result.get('mots_cles', []),
                    justification=result.get('justification', ''),
                    methode=result.get('methode', 'mistral_ollama')
                )
                
                classified_count += 1
            
            except Exception as e:
                errors += 1
                continue
        
        if classified_count > 0:
            print(f"   ✅ {classified_count} articles classifiés")
        if errors > 0:
            print(f"   ⚠️ {errors} erreurs")
    
    def scrape_all_sites(self, sites_file: str = None, days: int = 30) -> dict:
        """
        Scraper tous les sites depuis la table media (ou fichier en fallback)
        
        Args:
            sites_file: [DEPRECATED] Chemin vers le fichier contenant les URLs (pour compatibilité)
            days: Nombre de jours à récupérer
        
        Returns:
            Dictionnaire avec les statistiques
        """
        print("\n" + "="*60)
        print("🚀 MÉDIA-SCAN - Collecte Multi-Sites (depuis table media)")
        print("="*60)
        
        # Récupérer les médias depuis la base de données
        medias = self.db.get_medias_for_web_scraping(actif_only=True)
        
        if not medias:
            print("⚠️ Aucun média trouvé dans la table media")
            return {}
        
        print(f"\n📋 {len(medias)} sites à scraper")
        print(f"📅 Période: {days} derniers jours\n")
        
        # Statistiques
        stats = {
            'total_sites': len(medias),
            'success': 0,
            'errors': 0,
            'total_articles': 0,
            'by_method': {
                'html_scraping': 0,
                'rss_feed': 0,
                'error': 0
            },
            'details': []
        }
        
        # Scraper chaque site
        for i, media in enumerate(medias, 1):
            print(f"\n[{i}/{len(medias)}] Traitement de {media.nom} ({media.url})...")
            
            count, method, message = self.scrape_site(media.url, days=days)
            
            if count > 0:
                stats['success'] += 1
                stats['total_articles'] += count
            else:
                stats['errors'] += 1
            
            stats['by_method'][method] = stats['by_method'].get(method, 0) + count
            
            stats['details'].append({
                'media_id': media.id,
                'nom': media.nom,
                'url': media.url,
                'articles': count,
                'method': method,
                'message': message
            })
            
            print(message)
        
        # Afficher le résumé
        self._print_summary(stats)
        
        return stats
    
    def _print_summary(self, stats: dict):
        """Afficher le résumé de la collecte"""
        print("\n" + "="*60)
        print("📊 RÉSUMÉ DE LA COLLECTE")
        print("="*60)
        print(f"\n✅ Sites traités: {stats['total_sites']}")
        print(f"   • Succès: {stats['success']}")
        print(f"   • Erreurs: {stats['errors']}")
        print(f"\n📰 Total articles collectés: {stats['total_articles']}")
        print(f"\n🔧 Par méthode:")
        print(f"   • HTML Scraping: {stats['by_method'].get('html_scraping', 0)} articles")
        
        print(f"\n📋 Détails par site:")
        for detail in stats['details']:
            status = "✅" if detail['articles'] > 0 else "❌"
            print(f"   {status} {detail['url']}: {detail['articles']} articles ({detail['method']})")
        
        print("\n" + "="*60)
