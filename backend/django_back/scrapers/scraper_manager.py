"""
Gestionnaire principal de scraping avec fallback automatique
"""

from typing import List, Tuple
from urllib.parse import urlparse

from database.db_manager import DatabaseManager
from database.models import Article
from .wordpress_scraper import WordPressScraper
from .html_scraper import HTMLScraper


class ScraperManager:
    """Gestionnaire de scraping avec détection automatique et fallback"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialise le gestionnaire
        
        Args:
            db_manager: Instance de DatabaseManager
        """
        self.db = db_manager
    
    def scrape_site(self, url: str, days: int = 30) -> Tuple[int, str, str]:
        """
        Scraper un site avec détection automatique WordPress/HTML
        
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
        print(f"{'='*60}")
        
        # Tentative 1: WordPress API
        print("\n📡 Tentative 1: API WordPress...")
        try:
            wp_scraper = WordPressScraper(url)
            
            if wp_scraper.is_wordpress():
                print("✅ Site WordPress détecté!")
                
                # Ajouter/mettre à jour le média
                media_id = self.db.add_media(media_name, url, 'wordpress')
                
                # Scraper les articles
                articles = wp_scraper.scrape(media_id, days=days)
                
                # Si aucun article récupéré, peut-être que l'API est bloquée
                if len(articles) == 0:
                    print("⚠️ Aucun article récupéré via API WordPress (peut-être bloquée)")
                    print("   💡 Tentative de fallback vers HTML scraping...")
                else:
                    # Sauvegarder en base
                    saved_count = self._save_articles(articles)
                    
                    # Mettre à jour la date de dernière collecte
                    self.db.update_media_last_scrape(media_id)
                    
                    # Logger
                    self.db.add_scraping_log(
                        media_id=media_id,
                        status='success',
                        methode='wordpress_api',
                        articles_collectes=saved_count,
                        message=f"{saved_count} articles collectés via API WordPress"
                    )
                    
                    return saved_count, 'wordpress_api', f"✅ {saved_count} articles collectés via API WordPress"
            
            else:
                print("⚠️ Site non-WordPress ou API non accessible")
        
        except Exception as e:
            print(f"❌ Erreur WordPress API: {e}")
        
        # Tentative 2: Scraping HTML
        print("\n🌐 Tentative 2: Scraping HTML...")
        try:
            html_scraper = HTMLScraper(url)
            
            # Ajouter/mettre à jour le média
            media_id = self.db.add_media(media_name, url, 'html')
            
            # Scraper les articles
            articles = html_scraper.scrape(media_id, days=days, max_articles=50)
            
            # Sauvegarder en base
            saved_count = self._save_articles(articles)
            
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
            error_msg = f"❌ Erreur scraping HTML: {e}"
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
    
    def _save_articles(self, articles: List[Article]) -> int:
        """
        Sauvegarder les articles en base de données
        
        Args:
            articles: Liste d'articles à sauvegarder
        
        Returns:
            Nombre d'articles sauvegardés (nouveaux uniquement)
        """
        saved_count = 0
        duplicate_count = 0
        
        for article in articles:
            # Vérifier si l'article existe déjà
            if not self.db.article_exists(article.url):
                article_id = self.db.add_article(article)
                if article_id:
                    saved_count += 1
            else:
                duplicate_count += 1
        
        if duplicate_count > 0:
            print(f"   💾 {saved_count} nouveaux articles, {duplicate_count} doublons ignorés")
        
        return saved_count
    
    def scrape_all_sites(self, sites_file: str = 'sites.txt', days: int = 30) -> dict:
        """
        Scraper tous les sites listés dans un fichier
        
        Args:
            sites_file: Chemin vers le fichier contenant les URLs
            days: Nombre de jours à récupérer
        
        Returns:
            Dictionnaire avec les statistiques
        """
        print("\n" + "="*60)
        print("🚀 MÉDIA-SCAN - Collecte Multi-Sites")
        print("="*60)
        
        # Lire le fichier des sites
        try:
            with open(sites_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"❌ Fichier {sites_file} non trouvé")
            return {}
        
        # Filtrer les lignes (ignorer commentaires et lignes vides)
        urls = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
        
        print(f"\n📋 {len(urls)} sites à scraper")
        print(f"📅 Période: {days} derniers jours\n")
        
        # Statistiques
        stats = {
            'total_sites': len(urls),
            'success': 0,
            'errors': 0,
            'total_articles': 0,
            'by_method': {
                'wordpress_api': 0,
                'html_scraping': 0,
                'error': 0
            },
            'details': []
        }
        
        # Scraper chaque site
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Traitement de {url}...")
            
            count, method, message = self.scrape_site(url, days=days)
            
            if count > 0:
                stats['success'] += 1
                stats['total_articles'] += count
            else:
                stats['errors'] += 1
            
            stats['by_method'][method] = stats['by_method'].get(method, 0) + count
            
            stats['details'].append({
                'url': url,
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
        print(f"   • WordPress API: {stats['by_method'].get('wordpress_api', 0)} articles")
        print(f"   • HTML Scraping: {stats['by_method'].get('html_scraping', 0)} articles")
        
        print(f"\n📋 Détails par site:")
        for detail in stats['details']:
            status = "✅" if detail['articles'] > 0 else "❌"
            print(f"   {status} {detail['url']}: {detail['articles']} articles ({detail['method']})")
        
        print("\n" + "="*60)
