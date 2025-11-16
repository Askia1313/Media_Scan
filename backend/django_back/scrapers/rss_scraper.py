#!/usr/bin/env python3
"""
Scraper RSS pour récupérer les articles via les flux RSS
Plus rapide et plus fiable que le scraping HTML pur
"""

import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from database.models import Article


class RSScraper:
    """Scraper basé sur les flux RSS"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialise le scraper RSS
        
        Args:
            base_url: URL de base du site
            timeout: Timeout pour les requêtes HTTP
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.domain = urlparse(base_url).netloc
        
        # URLs RSS communes
        self.rss_urls = [
            f"{self.base_url}/feed/",
            f"{self.base_url}/feed",
            f"{self.base_url}/rss/",
            f"{self.base_url}/rss",
            f"{self.base_url}/atom.xml",
            f"{self.base_url}/rss.xml",
            f"{self.base_url}/feed.xml",
            f"{self.base_url}/index.rss",
            f"{self.base_url}/spip.php?page=backend",  # Pour SPIP (lefaso.net)
        ]
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def find_rss_feed(self) -> Optional[str]:
        """
        Trouver automatiquement le flux RSS du site
        
        Returns:
            URL du flux RSS ou None
        """
        print(f"   🔍 Recherche du flux RSS...")
        
        # Tester les URLs RSS communes
        for rss_url in self.rss_urls:
            try:
                response = self.session.get(rss_url, timeout=self.timeout)
                if response.status_code == 200:
                    # Vérifier que c'est bien un flux RSS/Atom
                    content_type = response.headers.get('content-type', '').lower()
                    if 'xml' in content_type or 'rss' in content_type or 'atom' in content_type:
                        print(f"   ✅ Flux RSS trouvé: {rss_url}")
                        return rss_url
                    
                    # Vérifier le contenu
                    if b'<rss' in response.content or b'<feed' in response.content:
                        print(f"   ✅ Flux RSS trouvé: {rss_url}")
                        return rss_url
            except:
                continue
        
        # Chercher dans la page d'accueil
        try:
            response = self.session.get(self.base_url, timeout=self.timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Chercher les balises <link> avec type RSS/Atom
                for link in soup.find_all('link', type=['application/rss+xml', 'application/atom+xml']):
                    href = link.get('href')
                    if href:
                        if not href.startswith('http'):
                            href = f"{self.base_url}{href}" if href.startswith('/') else f"{self.base_url}/{href}"
                        print(f"   ✅ Flux RSS trouvé dans la page: {href}")
                        return href
        except:
            pass
        
        print(f"   ❌ Aucun flux RSS trouvé")
        return None
    
    def parse_rss_date(self, date_str: str) -> Optional[datetime]:
        """
        Parser une date RSS (format RFC 822 ou ISO 8601)
        
        Args:
            date_str: Date au format RSS
        
        Returns:
            Objet datetime ou None
        """
        if not date_str:
            return None
        
        try:
            # feedparser parse automatiquement les dates
            import time
            parsed = feedparser._parse_date(date_str)
            if parsed:
                return datetime(*parsed[:6])
        except:
            pass
        
        # Fallback: essayer différents formats
        formats = [
            '%a, %d %b %Y %H:%M:%S %z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.replace(tzinfo=None) if dt.tzinfo else dt
            except:
                continue
        
        return None
    
    def get_articles_from_rss(self, days: int = 30, max_articles: int = 100) -> List[dict]:
        """
        Récupérer les articles depuis le flux RSS
        
        Args:
            days: Nombre de jours dans le passé
            max_articles: Nombre maximum d'articles
        
        Returns:
            Liste de dictionnaires avec les infos des articles
        """
        # Trouver le flux RSS
        rss_url = self.find_rss_feed()
        if not rss_url:
            return []
        
        print(f"   📡 Lecture du flux RSS...")
        
        try:
            # Parser le flux RSS
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                print(f"   ⚠️ Aucune entrée dans le flux RSS")
                return []
            
            print(f"   📊 {len(feed.entries)} entrées trouvées dans le flux")
            
            # Date limite
            date_limit = datetime.now() - timedelta(days=days)
            
            articles = []
            for entry in feed.entries[:max_articles]:
                try:
                    # Extraire les informations
                    titre = entry.get('title', '').strip()
                    url = entry.get('link', '').strip()
                    
                    if not titre or not url:
                        continue
                    
                    # Date de publication
                    date_pub = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        date_pub = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        date_pub = datetime(*entry.updated_parsed[:6])
                    elif hasattr(entry, 'published'):
                        date_pub = self.parse_rss_date(entry.published)
                    
                    # Filtrer par date
                    if date_pub and date_pub < date_limit:
                        continue
                    
                    # Résumé/description
                    description = ''
                    if hasattr(entry, 'summary'):
                        description = entry.summary
                    elif hasattr(entry, 'description'):
                        description = entry.description
                    
                    # Nettoyer le HTML du résumé
                    if description:
                        soup = BeautifulSoup(description, 'html.parser')
                        description = soup.get_text().strip()
                    
                    # Auteur
                    auteur = None
                    if hasattr(entry, 'author'):
                        auteur = entry.author
                    elif hasattr(entry, 'dc_creator'):
                        auteur = entry.dc_creator
                    
                    # Image
                    image_url = None
                    if hasattr(entry, 'media_content') and entry.media_content:
                        image_url = entry.media_content[0].get('url')
                    elif hasattr(entry, 'enclosures') and entry.enclosures:
                        for enclosure in entry.enclosures:
                            if 'image' in enclosure.get('type', ''):
                                image_url = enclosure.get('href')
                                break
                    
                    # Catégories
                    categories = []
                    if hasattr(entry, 'tags'):
                        categories = [tag.term for tag in entry.tags]
                    
                    articles.append({
                        'titre': titre,
                        'url': url,
                        'date_publication': date_pub,
                        'description': description,
                        'auteur': auteur,
                        'image_url': image_url,
                        'categories': categories,
                    })
                
                except Exception as e:
                    print(f"   ⚠️ Erreur parsing entrée RSS: {e}")
                    continue
            
            print(f"   ✅ {len(articles)} articles récents trouvés")
            return articles
        
        except Exception as e:
            print(f"   ❌ Erreur lecture flux RSS: {e}")
            return []
    
    def scrape_article_content(self, url: str) -> Optional[str]:
        """
        Scraper le contenu complet d'un article depuis son URL
        
        Args:
            url: URL de l'article
        
        Returns:
            Contenu de l'article ou None
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Sélecteurs pour le contenu principal
            content_selectors = [
                'article .entry-content',
                'article .post-content',
                '.article-content',
                '.post-content',
                '.entry-content',
                'article .content',
                '[itemprop="articleBody"]',
                '.article-body',
                'main article',
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # Nettoyer le contenu
                    for tag in content_elem.find_all(['script', 'style', 'iframe', 'nav', 'aside']):
                        tag.decompose()
                    
                    text = content_elem.get_text(separator='\n', strip=True)
                    if len(text) > 100:  # Au moins 100 caractères
                        return text
            
            # Fallback: chercher tous les paragraphes dans article
            article_elem = soup.find('article')
            if article_elem:
                paragraphs = article_elem.find_all('p')
                text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
                if len(text) > 100:
                    return text
            
            return None
        
        except Exception as e:
            return None
    
    def scrape(self, media_id: int, days: int = 30, max_articles: int = 100) -> List[Article]:
        """
        Scraper les articles via RSS
        
        Args:
            media_id: ID du média en base de données
            days: Nombre de jours dans le passé
            max_articles: Nombre maximum d'articles
        
        Returns:
            Liste d'objets Article
        """
        print(f"🌐 Scraping RSS depuis {self.base_url}...")
        
        # Récupérer les articles du flux RSS
        rss_articles = self.get_articles_from_rss(days, max_articles)
        
        if not rss_articles:
            print(f"   ⚠️ Aucun article trouvé dans le flux RSS")
            return []
        
        articles = []
        
        print(f"   📄 Scraping du contenu complet...")
        for i, rss_article in enumerate(rss_articles, 1):
            try:
                print(f"   Article {i}/{len(rss_articles)}: {rss_article['url'][:80]}...")
                
                # Scraper le contenu complet
                contenu = self.scrape_article_content(rss_article['url'])
                
                # Si pas de contenu, utiliser la description du RSS
                if not contenu:
                    contenu = rss_article.get('description', '')
                
                if not contenu or len(contenu) < 50:
                    print(f"      ⚠️ Contenu trop court, ignoré")
                    continue
                
                # Créer l'objet Article
                article = Article(
                    media_id=media_id,
                    titre=rss_article['titre'],
                    contenu=contenu,
                    url=rss_article['url'],
                    date_publication=rss_article.get('date_publication') or datetime.now(),
                    auteur=rss_article.get('auteur'),
                    image_url=rss_article.get('image_url'),
                    source_type='rss_feed'
                )
                
                articles.append(article)
            
            except Exception as e:
                print(f"      ⚠️ Erreur scraping article: {e}")
                continue
        
        print(f"✅ {len(articles)} articles scrapés avec succès")
        return articles
