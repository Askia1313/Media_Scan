"""
Scraper pour les sites WordPress via l'API REST
"""

import requests
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin
import time

from database.models import Article


class WordPressScraper:
    """Scraper pour les sites WordPress utilisant l'API REST"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialise le scraper WordPress
        
        Args:
            base_url: URL de base du site (ex: https://lefaso.net)
            timeout: Timeout pour les requêtes HTTP (en secondes)
        """
        self.base_url = base_url.rstrip('/')
        self.api_root = f"{self.base_url}/wp-json/"  # Endpoint racine pour détection
        self.api_url = f"{self.base_url}/wp-json/wp/v2/"  # Endpoint pour les posts
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def is_wordpress(self) -> bool:
        """
        Vérifier si le site utilise WordPress et si l'API est accessible
        
        Returns:
            True si WordPress est détecté ET l'API est accessible, False sinon
        """
        try:
            # Debug: Afficher l'URL testée
            print(f"   🔍 Test API: {self.api_root}")
            
            # Tester l'endpoint RACINE de l'API WordPress (/wp-json/)
            response = self.session.get(
                self.api_root,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            # Debug: Afficher le status code
            print(f"   📡 Status: {response.status_code}")
            
            # L'API WordPress retourne un JSON avec les namespaces
            if response.status_code == 200:
                try:
                    data = response.json()
                    has_namespaces = 'namespaces' in data
                    has_wp_v2 = 'wp/v2' in data.get('namespaces', [])
                    
                    # Debug: Afficher les détails
                    if has_namespaces:
                        print(f"   ✅ Namespaces trouvés: {data.get('namespaces', [])}")
                    else:
                        print(f"   ❌ Pas de 'namespaces' dans la réponse")
                        print(f"   📄 Clés disponibles: {list(data.keys())[:5]}")
                    
                    if has_namespaces and has_wp_v2:
                        # WordPress détecté, maintenant tester l'accès aux posts
                        print(f"   🔍 Test accès posts: {self.api_url}posts?per_page=1")
                        posts_response = self.session.get(
                            f"{self.api_url}posts?per_page=1",
                            timeout=self.timeout
                        )
                        
                        if posts_response.status_code == 401:
                            print(f"   ❌ API bloquée (401) - Basculement vers HTML scraping")
                            return False
                        elif posts_response.status_code == 200:
                            print(f"   ✅ API posts accessible")
                            return True
                        else:
                            print(f"   ⚠️ Status posts: {posts_response.status_code}")
                            return True  # On essaie quand même
                    
                    return False
                
                except ValueError as e:
                    print(f"   ❌ Réponse non-JSON: {response.text[:200]}")
                    return False
            else:
                print(f"   ❌ Status {response.status_code} - Pas WordPress")
            
            return False
        
        except requests.exceptions.Timeout:
            print(f"   ⏱️ Timeout après {self.timeout}s")
            return False
        
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ Erreur de connexion: {e}")
            return False
        
        except Exception as e:
            print(f"   ⚠️ Erreur détection WordPress: {type(e).__name__}: {e}")
            return False
    
    def get_posts(self, days: int = 30, per_page: int = 100, max_pages: int = 5) -> List[Dict[str, Any]]:
        """
        Récupérer les articles via l'API WordPress
        
        Args:
            days: Nombre de jours dans le passé
            per_page: Nombre d'articles par page
            max_pages: Nombre maximum de pages à récupérer
        
        Returns:
            Liste des articles bruts de l'API
        """
        all_posts = []
        
        # Calculer la date limite (30 jours en arrière)
        date_limit = datetime.now() - timedelta(days=days)
        # Format ISO 8601 avec timezone UTC (requis par WordPress)
        date_limit_str = date_limit.strftime('%Y-%m-%dT%H:%M:%S')
        
        print(f"📡 Récupération articles WordPress depuis {self.base_url}...")
        print(f"   📅 Articles après le: {date_limit.strftime('%Y-%m-%d')}")
        
        for page in range(1, max_pages + 1):
            try:
                # Paramètres de la requête
                params = {
                    'per_page': per_page,
                    'page': page,
                    # Note: Le paramètre 'after' ne fonctionne pas sur tous les sites
                    # On filtre côté client à la place
                    'orderby': 'date',
                    'order': 'desc',
                    '_embed': 'true'  # Inclure les médias et auteurs
                }
                
                response = self.session.get(
                    urljoin(self.api_url, 'posts'),
                    params=params,
                    timeout=self.timeout
                )
                
                # Gestion de l'erreur 401 (API bloquée par iThemes Security ou autre)
                if response.status_code == 401:
                    try:
                        error_data = response.json()
                        error_code = error_data.get('code', '')
                        error_message = error_data.get('message', '')
                        
                        if 'itsec' in error_code or 'security' in error_message.lower():
                            print(f"   ❌ API WordPress bloquée par plugin de sécurité (iThemes Security)")
                            print(f"   💡 Le site utilise WordPress mais l'API REST est protégée")
                        else:
                            print(f"   ❌ Erreur 401: Accès non autorisé à l'API")
                    except:
                        print(f"   ❌ Erreur HTTP 401: Accès non autorisé")
                    
                    # Arrêter et retourner une liste vide
                    print(f"✅ Total: 0 articles récupérés (API protégée)")
                    return all_posts
                
                if response.status_code == 200:
                    posts = response.json()
                    
                    if not posts:
                        print(f"   Page {page}: Aucun article")
                        break
                    
                    # Filtrer les articles par date (vérification côté client)
                    filtered_posts = []
                    articles_too_old = 0
                    
                    for post in posts:
                        try:
                            post_date_str = post.get('date', '')
                            if post_date_str:
                                # Parser la date de l'article
                                post_date = datetime.fromisoformat(post_date_str.replace('Z', '+00:00'))
                                # Enlever timezone pour comparaison
                                post_date_naive = post_date.replace(tzinfo=None)
                                date_limit_naive = date_limit.replace(tzinfo=None) if hasattr(date_limit, 'tzinfo') else date_limit
                                
                                # Vérifier si l'article est dans la période
                                if post_date_naive >= date_limit_naive:
                                    filtered_posts.append(post)
                                else:
                                    articles_too_old += 1
                            else:
                                # Si pas de date, on garde l'article
                                filtered_posts.append(post)
                        except Exception as e:
                            # En cas d'erreur de parsing, on garde l'article
                            filtered_posts.append(post)
                    
                    all_posts.extend(filtered_posts)
                    
                    if articles_too_old > 0:
                        print(f"   Page {page}: {len(filtered_posts)}/{len(posts)} articles récents ({articles_too_old} trop anciens)")
                    else:
                        print(f"   Page {page}: {len(filtered_posts)} articles récupérés")
                    
                    # Si tous les articles sont trop anciens, arrêter
                    if len(filtered_posts) == 0 and articles_too_old > 0:
                        print(f"   Page {page}: Tous les articles sont trop anciens, arrêt")
                        break
                    
                    # Pause pour ne pas surcharger le serveur
                    time.sleep(1)
                
                elif response.status_code == 400:
                    # Page hors limites
                    print(f"   Page {page}: Fin de pagination")
                    break
                
                else:
                    print(f"   Page {page}: Erreur HTTP {response.status_code}")
                    break
            
            except Exception as e:
                print(f"   Page {page}: Erreur - {e}")
                break
        
        total_retrieved = len(all_posts)
        print(f"✅ Total: {total_retrieved} articles récupérés")
        
        if total_retrieved > 0:
            print(f"   📊 Période demandée: {days} derniers jours (depuis {date_limit.strftime('%Y-%m-%d')})")
        
        return all_posts
    
    def parse_post(self, post_data: Dict[str, Any], media_id: int) -> Article:
        """
        Convertir un post WordPress en objet Article
        
        Args:
            post_data: Données brutes de l'API WordPress
            media_id: ID du média dans notre base
        
        Returns:
            Instance d'Article
        """
        # Extraire le contenu HTML et le nettoyer
        contenu_html = post_data.get('content', {}).get('rendered', '')
        contenu_text = self._strip_html(contenu_html)
        
        # Extraire l'extrait
        extrait_html = post_data.get('excerpt', {}).get('rendered', '')
        extrait_text = self._strip_html(extrait_html)
        
        # Extraire l'auteur (si disponible dans _embedded)
        auteur = None
        if '_embedded' in post_data and 'author' in post_data['_embedded']:
            authors = post_data['_embedded']['author']
            if authors:
                auteur = authors[0].get('name')
        
        # Extraire l'image à la une
        image_url = None
        if '_embedded' in post_data and 'wp:featuredmedia' in post_data['_embedded']:
            featured_media = post_data['_embedded']['wp:featuredmedia']
            if featured_media:
                image_url = featured_media[0].get('source_url')
        
        # Extraire les catégories
        categories = []
        if '_embedded' in post_data and 'wp:term' in post_data['_embedded']:
            terms = post_data['_embedded']['wp:term']
            for term_group in terms:
                for term in term_group:
                    if term.get('taxonomy') == 'category':
                        categories.append(term.get('name'))
        
        # Extraire les tags
        tags = []
        if '_embedded' in post_data and 'wp:term' in post_data['_embedded']:
            terms = post_data['_embedded']['wp:term']
            for term_group in terms:
                for term in term_group:
                    if term.get('taxonomy') == 'post_tag':
                        tags.append(term.get('name'))
        
        # Parser la date de publication
        date_pub = None
        if 'date' in post_data:
            try:
                date_pub = datetime.fromisoformat(post_data['date'].replace('Z', '+00:00'))
            except:
                pass
        
        return Article(
            media_id=media_id,
            titre=self._strip_html(post_data.get('title', {}).get('rendered', '')),
            contenu=contenu_text,
            extrait=extrait_text,
            url=post_data.get('link', ''),
            auteur=auteur,
            date_publication=date_pub,
            image_url=image_url,
            categories=categories,
            tags=tags,
            source_type='wordpress_api',
            commentaires=post_data.get('comment_count', 0)
        )
    
    def scrape(self, media_id: int, days: int = 30) -> List[Article]:
        """
        Scraper les articles d'un site WordPress
        
        Args:
            media_id: ID du média dans notre base
            days: Nombre de jours à récupérer
        
        Returns:
            Liste d'objets Article
        """
        # Vérifier si c'est bien un site WordPress
        if not self.is_wordpress():
            raise Exception("Ce site n'utilise pas WordPress ou l'API n'est pas accessible")
        
        # Récupérer les posts
        posts_data = self.get_posts(days=days)
        
        # Convertir en objets Article
        articles = []
        for post_data in posts_data:
            try:
                article = self.parse_post(post_data, media_id)
                articles.append(article)
            except Exception as e:
                print(f"⚠️ Erreur parsing article: {e}")
                continue
        
        return articles
    
    @staticmethod
    def _strip_html(html: str) -> str:
        """
        Nettoyer le HTML pour extraire le texte
        
        Args:
            html: Contenu HTML
        
        Returns:
            Texte sans balises HTML
        """
        from html.parser import HTMLParser
        
        class HTMLStripper(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
            
            def handle_data(self, data):
                self.text.append(data)
            
            def get_text(self):
                return ''.join(self.text)
        
        stripper = HTMLStripper()
        try:
            stripper.feed(html)
            return stripper.get_text().strip()
        except:
            return html
