"""
Scraper HTML générique (fallback quand WordPress API n'est pas disponible)
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin, urlparse
import time
import re

from database.models import Article


class HTMLScraper:
    """Scraper HTML générique pour sites non-WordPress"""
    
    def __init__(self, base_url: str, timeout: int = 10):
        """
        Initialise le scraper HTML
        
        Args:
            base_url: URL de base du site
            timeout: Timeout pour les requêtes HTTP
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Récupérer et parser une page HTML
        
        Args:
            url: URL de la page
        
        Returns:
            Objet BeautifulSoup ou None en cas d'erreur
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            return BeautifulSoup(response.content, 'lxml')
        
        except Exception as e:
            print(f"⚠️ Erreur récupération page {url}: {e}")
            return None
    
    def find_article_links(self, soup: BeautifulSoup) -> List[str]:
        """
        Trouver les liens vers les articles sur une page
        
        Args:
            soup: Objet BeautifulSoup de la page
        
        Returns:
            Liste d'URLs d'articles
        """
        links = []
        
        # Sélecteurs communs pour les articles
        selectors = [
            'article a[href]',
            '.post a[href]',
            '.entry a[href]',
            '.article-item a[href]',
            '.news-item a[href]',
            'h2 a[href]',
            'h3 a[href]',
            '.entry-title a[href]',
            '.post-title a[href]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for elem in elements:
                href = elem.get('href')
                if href:
                    # Convertir en URL absolue
                    full_url = urljoin(self.base_url, href)
                    
                    # Vérifier que c'est un lien interne
                    if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                        # Éviter les doublons
                        if full_url not in links and self._is_article_url(full_url):
                            links.append(full_url)
        
        return list(set(links))  # Supprimer les doublons
    
    def _is_article_url(self, url: str) -> bool:
        """
        Vérifier si une URL semble être un article
        
        Args:
            url: URL à vérifier
        
        Returns:
            True si c'est probablement un article
        """
        # Exclure les URLs non-articles
        excluded_patterns = [
            '/category/', '/tag/', '/author/', '/page/',
            '/wp-admin/', '/wp-content/', '/wp-includes/',
            '.jpg', '.png', '.gif', '.pdf', '.css', '.js',
            '/contact', '/about', '/mentions-legales'
        ]
        
        url_lower = url.lower()
        for pattern in excluded_patterns:
            if pattern in url_lower:
                return False
        
        return True
    
    def scrape_article(self, url: str, media_id: int) -> Optional[Article]:
        """
        Scraper un article individuel
        
        Args:
            url: URL de l'article
            media_id: ID du média
        
        Returns:
            Objet Article ou None
        """
        soup = self.get_page(url)
        if not soup:
            return None
        
        try:
            # Extraire le titre
            titre = self._extract_title(soup)
            if not titre:
                return None
            
            # Extraire le contenu
            contenu = self._extract_content(soup)
            if not contenu or len(contenu) < 100:  # Minimum 100 caractères
                return None
            
            # Extraire les métadonnées
            date_pub = self._extract_date(soup)
            auteur = self._extract_author(soup)
            image_url = self._extract_image(soup)
            extrait = contenu[:300] + '...' if len(contenu) > 300 else contenu
            
            return Article(
                media_id=media_id,
                titre=titre,
                contenu=contenu,
                extrait=extrait,
                url=url,
                auteur=auteur,
                date_publication=date_pub,
                image_url=image_url,
                source_type='html_scraping'
            )
        
        except Exception as e:
            print(f"⚠️ Erreur scraping article {url}: {e}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extraire le titre de l'article"""
        # Essayer différents sélecteurs
        selectors = [
            'h1.entry-title',
            'h1.post-title',
            'h1.article-title',
            'article h1',
            '.post h1',
            'h1'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        
        # Fallback: titre de la page
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        return None
    
    def _extract_content(self, soup: BeautifulSoup) -> Optional[str]:
        """Extraire le contenu de l'article"""
        # Essayer différents sélecteurs
        selectors = [
            'article .entry-content',
            'article .post-content',
            'article .article-content',
            '.post-content',
            '.entry-content',
            '.article-body',
            'article',
            '.post'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                # Supprimer les scripts et styles
                for script in elem(['script', 'style', 'iframe', 'nav', 'aside']):
                    script.decompose()
                
                # Extraire le texte
                paragraphs = elem.find_all('p')
                if paragraphs:
                    text = ' '.join([p.get_text(strip=True) for p in paragraphs])
                    if len(text) > 100:
                        return text
        
        return None
    
    def _extract_date(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Extraire la date de publication"""
        # Essayer les balises time
        time_elem = soup.find('time')
        if time_elem:
            datetime_attr = time_elem.get('datetime')
            if datetime_attr:
                try:
                    return datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                except:
                    pass
        
        # Essayer les métadonnées
        meta_date = soup.find('meta', {'property': 'article:published_time'})
        if meta_date:
            try:
                return datetime.fromisoformat(meta_date.get('content').replace('Z', '+00:00'))
            except:
                pass
        
        # Essayer de trouver une date dans le texte
        date_patterns = [
            r'(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})',
            r'(\d{4})-(\d{2})-(\d{2})',
            r'(\d{2})/(\d{2})/(\d{4})'
        ]
        
        text = soup.get_text()
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    # Parsing basique (à améliorer)
                    return datetime.now()  # Placeholder
                except:
                    pass
        
        # Par défaut: date actuelle
        return datetime.now()
    
    def _extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """Extraire l'auteur"""
        # Essayer différents sélecteurs
        selectors = [
            '.author-name',
            '.post-author',
            '.entry-author',
            'span.author',
            'a[rel="author"]'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        
        # Essayer les métadonnées
        meta_author = soup.find('meta', {'name': 'author'})
        if meta_author:
            return meta_author.get('content')
        
        return None
    
    def _extract_image(self, soup: BeautifulSoup) -> Optional[str]:
        """Extraire l'image principale"""
        # Essayer Open Graph
        og_image = soup.find('meta', {'property': 'og:image'})
        if og_image:
            return og_image.get('content')
        
        # Essayer la première image dans l'article
        article = soup.find('article') or soup.find(class_='post')
        if article:
            img = article.find('img')
            if img:
                src = img.get('src') or img.get('data-src')
                if src:
                    return urljoin(self.base_url, src)
        
        return None
    
    def scrape(self, media_id: int, days: int = 30, max_articles: int = 50) -> List[Article]:
        """
        Scraper les articles d'un site
        
        Args:
            media_id: ID du média
            days: Nombre de jours (utilisé pour filtrer si possible)
            max_articles: Nombre maximum d'articles à récupérer
        
        Returns:
            Liste d'objets Article
        """
        print(f"🌐 Scraping HTML depuis {self.base_url}...")
        
        # Récupérer la page d'accueil
        soup = self.get_page(self.base_url)
        if not soup:
            return []
        
        # Trouver les liens d'articles
        article_links = self.find_article_links(soup)
        print(f"   {len(article_links)} liens d'articles trouvés")
        
        # Limiter le nombre d'articles
        article_links = article_links[:max_articles]
        
        # Scraper chaque article
        articles = []
        for i, link in enumerate(article_links, 1):
            print(f"   Article {i}/{len(article_links)}: {link}")
            
            article = self.scrape_article(link, media_id)
            if article:
                articles.append(article)
            
            # Pause pour ne pas surcharger le serveur
            time.sleep(2)
        
        print(f"✅ {len(articles)} articles scrapés avec succès")
        return articles
