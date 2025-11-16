"""
Scraper HTML intelligent et ultra-performant
Fonctionne sur n'importe quel site, n'importe quelle technologie
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Set
from urllib.parse import urljoin, urlparse
import time
import re
from dateutil import parser as date_parser
import locale

from database.models import Article


class SmartHTMLScraper:
    """Scraper HTML intelligent et générique"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialise le scraper HTML intelligent
        
        Args:
            base_url: URL de base du site
            timeout: Timeout pour les requêtes HTTP (en secondes)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.domain = urlparse(base_url).netloc
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
            Objet BeautifulSoup ou None
        """
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            # Utiliser response.text au lieu de response.content pour gérer l'encodage
            soup = BeautifulSoup(response.text, 'html.parser')
            # Debug: vérifier que le parsing fonctionne
            test_links = soup.find_all('a')
            if len(test_links) == 0:
                print(f"   ⚠️ Warning: Aucun lien trouvé dans le HTML parsé (taille: {len(response.text)} chars)")
            return soup
        except Exception as e:
            print(f"⚠️ Erreur récupération page {url}: {e}")
            return None
    
    def find_article_links(self, soup: BeautifulSoup, max_links: int = 100) -> List[str]:
        """
        Trouver intelligemment les liens vers les articles
        
        Args:
            soup: Objet BeautifulSoup de la page
            max_links: Nombre maximum de liens à retourner
        
        Returns:
            Liste d'URLs d'articles
        """
        links = []
        seen_urls: Set[str] = set()
        
        # Sélecteurs CSS pour trouver les articles (du plus spécifique au plus général)
        selectors = [
            # Sélecteurs WordPress et CMS courants
            'article.post a[href]',
            'article a.entry-title[href]',
            '.post-item a[href]',
            '.entry-title a[href]',
            '.post-title a[href]',
            'article h2 a[href]',
            'article h3 a[href]',
            
            # Sélecteurs génériques
            'article a[href]',
            '.article a[href]',
            '.news-item a[href]',
            '.post a[href]',
            '.entry a[href]',
            
            # Sélecteurs par structure
            'main article a[href]',
            '.content article a[href]',
            '#content article a[href]',
            
            # Titres dans des conteneurs d'articles
            'h2.entry-title a[href]',
            'h3.entry-title a[href]',
            'h2 a[href]',
            'h3 a[href]',
            
            # URLs avec dates (structure /YYYY/MM/DD/ ou /YYYY/MM/)
            'a[href*="/202"]',  # Articles de 2020-2029
        ]
        
        print(f"   🔍 Recherche de liens d'articles...")
        
        # Recherche directe de tous les liens
        all_links = soup.find_all('a', href=True)
        print(f"   📊 {len(all_links)} liens trouvés au total")
        
        for link in all_links:
            if len(links) >= max_links:
                break
                
            href = link.get('href')
            if not href:
                continue
            
            # Convertir en URL absolue
            full_url = urljoin(self.base_url, href)
            
            # Vérifier que c'est un lien interne
            if urlparse(full_url).netloc != self.domain:
                continue
            
            # Éviter les doublons
            if full_url in seen_urls:
                continue
            
            # Vérifier que c'est probablement un article
            if self._is_article_url(full_url):
                links.append(full_url)
                seen_urls.add(full_url)
        
        print(f"   ✅ {len(links)} liens d'articles trouvés")
        return links
    
    def _is_article_url(self, url: str) -> bool:
        """
        Vérifier intelligemment si une URL est un article
        
        Args:
            url: URL à vérifier
        
        Returns:
            True si c'est probablement un article
        """
        url_lower = url.lower()
        
        # Patterns à exclure (pages système, médias, etc.)
        excluded_patterns = [
            # Pages système
            '/wp-admin', '/wp-content', '/wp-includes', '/wp-json',
            '/feed', '/rss', '/atom',
            '/cdn-cgi/', '/cgi-bin/',
            
            # Pages de navigation
            '/category/', '/categories/', '/tag/', '/tags/',
            '/author/', '/authors/', '/page/', '/search/',
            '/archives/', '/archive/',
            
            # Pages statiques
            '/contact', '/about', '/a-propos', '/qui-sommes-nous',
            '/mentions-legales', '/politique', '/privacy',
            '/conditions', '/terms', '/legal',
            '/notre-equipe', '/equipe', '/service',
            '/nous-ecrire', '/mon-compte', '/login', '/register',
            
            # Fichiers médias
            '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx',
            '.zip', '.rar', '.tar', '.gz',
            '.mp3', '.mp4', '.avi', '.mov',
            '.css', '.js', '.json', '.xml',
            
            # Autres
            '/comments', '/comment', '/reply',
            '#comment', '#respond',
        ]
        
        for pattern in excluded_patterns:
            if pattern in url_lower:
                return False
        
        # Exclure les URLs d'archives (qui se terminent par /YYYY/MM/ ou /YYYY/)
        if re.search(r'/\d{4}(/\d{2})?/?$', url):
            return False
        
        # Exclure les URLs trop courtes (juste le domaine)
        path = urlparse(url).path.strip('/')
        if not path or path == '':
            return False
        
        # L'URL doit avoir au moins un segment significatif
        path_segments = [s for s in path.split('/') if s]
        if len(path_segments) < 1:
            return False
        
        # Si l'URL contient une année, vérifier qu'il y a un titre après
        if re.search(r'/\d{4}/', url):
            # Doit avoir au moins 3 segments après l'année: /YYYY/MM/titre/ ou /YYYY/MM/DD/titre/
            all_segments = [s for s in path.split('/') if s]
            year_index = -1
            for i, seg in enumerate(all_segments):
                if re.match(r'^\d{4}$', seg):
                    year_index = i
                    break
            
            if year_index >= 0:
                # Il doit y avoir au moins un segment après l'année (le titre)
                if year_index >= len(all_segments) - 1:
                    return False
        
        return True
    
    def scrape_article(self, url: str, media_id: int, date_limit: datetime) -> Optional[Article]:
        """
        Scraper un article individuel avec extraction intelligente
        
        Args:
            url: URL de l'article
            media_id: ID du média
            date_limit: Date limite (30 jours)
        
        Returns:
            Objet Article ou None
        """
        soup = self.get_page(url)
        if not soup:
            return None
        
        try:
            # Extraction du titre
            titre = self._extract_title(soup)
            if not titre:
                return None
            
            # Extraction de la date
            date_publication = self._extract_date(soup, url)
            
            # Vérifier si l'article est dans la période (30 derniers jours)
            if date_publication:
                # Enlever la timezone pour comparaison
                date_pub_naive = date_publication.replace(tzinfo=None) if date_publication.tzinfo else date_publication
                if date_pub_naive < date_limit:
                    return None  # Article trop ancien
            
            # Extraction du contenu
            contenu = self._extract_content(soup)
            
            # Extraction de l'auteur
            auteur = self._extract_author(soup)
            
            # Extraction de l'image
            image_url = self._extract_image(soup)
            
            return Article(
                media_id=media_id,
                titre=titre,
                contenu=contenu,
                url=url,
                date_publication=date_publication or datetime.now(),
                auteur=auteur,
                image_url=image_url,
                source_type='html_scraping'
            )
        
        except Exception as e:
            print(f"   ⚠️ Erreur extraction article {url}: {e}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extraire le titre de l'article"""
        # Sélecteurs pour le titre (du plus spécifique au plus général)
        selectors = [
            'article h1',
            '.entry-title',
            '.post-title',
            'h1.title',
            'h1.article-title',
            '.article-header h1',
            'header h1',
            'h1',
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                titre = elem.get_text(strip=True)
                if titre and len(titre) > 10:  # Titre significatif
                    return titre
        
        # Fallback: meta title ou title
        meta_title = soup.find('meta', property='og:title')
        if meta_title and meta_title.get('content'):
            return meta_title['content']
        
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True).split('|')[0].split('-')[0].strip()
        
        return None
    
    def _extract_date(self, soup: BeautifulSoup, url: str) -> Optional[datetime]:
        """Extraire intelligemment la date de publication"""
        
        # 1. Chercher dans les meta tags
        meta_selectors = [
            ('meta', 'property', 'article:published_time'),
            ('meta', 'property', 'og:published_time'),
            ('meta', 'name', 'publish_date'),
            ('meta', 'name', 'date'),
            ('meta', 'itemprop', 'datePublished'),
        ]
        
        for tag, attr, value in meta_selectors:
            elem = soup.find(tag, {attr: value})
            if elem and elem.get('content'):
                try:
                    return date_parser.parse(elem['content'])
                except:
                    pass
        
        # 2. Chercher dans les éléments time
        time_elem = soup.find('time', datetime=True)
        if time_elem:
            try:
                return date_parser.parse(time_elem['datetime'])
            except:
                pass
        
        # 3. Chercher dans les classes/IDs courants
        date_selectors = [
            '.entry-date',
            '.post-date',
            '.published',
            '.date',
            'time',
            '.article-date',
            'span.date',
        ]
        
        for selector in date_selectors:
            elem = soup.select_one(selector)
            if elem:
                date_text = elem.get_text(strip=True)
                date_obj = self._parse_french_date(date_text)
                if date_obj:
                    return date_obj
        
        # 4. Extraire de l'URL (structure /YYYY/MM/DD/)
        url_date = self._extract_date_from_url(url)
        if url_date:
            return url_date
        
        return None
    
    def _parse_french_date(self, date_text: str) -> Optional[datetime]:
        """Parser une date en français"""
        try:
            # Nettoyer le texte
            date_text = date_text.strip()
            
            # Essayer le parser automatique
            return date_parser.parse(date_text, fuzzy=True)
        except:
            pass
        
        # Patterns français courants
        patterns = [
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # DD/MM/YYYY ou DD-MM-YYYY
            r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # YYYY/MM/DD ou YYYY-MM-DD
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_text)
            if match:
                try:
                    groups = match.groups()
                    if len(groups[0]) == 4:  # YYYY-MM-DD
                        return datetime(int(groups[0]), int(groups[1]), int(groups[2]))
                    else:  # DD-MM-YYYY
                        return datetime(int(groups[2]), int(groups[1]), int(groups[0]))
                except:
                    pass
        
        return None
    
    def _extract_date_from_url(self, url: str) -> Optional[datetime]:
        """Extraire la date depuis l'URL"""
        # Pattern: /YYYY/MM/DD/ ou /YYYY/MM/
        match = re.search(r'/(\d{4})/(\d{2})(?:/(\d{2}))?/', url)
        if match:
            try:
                year = int(match.group(1))
                month = int(match.group(2))
                day = int(match.group(3)) if match.group(3) else 1
                return datetime(year, month, day)
            except:
                pass
        
        return None
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extraire le contenu de l'article"""
        # Sélecteurs pour le contenu
        selectors = [
            'article .entry-content',
            'article .post-content',
            'article .content',
            '.entry-content',
            '.post-content',
            '.article-content',
            'article',
            '.content',
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                # Supprimer les scripts, styles, etc.
                for tag in elem.find_all(['script', 'style', 'iframe', 'nav', 'aside']):
                    tag.decompose()
                
                content = elem.get_text(separator='\n', strip=True)
                if content and len(content) > 100:  # Contenu significatif
                    return content[:5000]  # Limiter à 5000 caractères
        
        return ""
    
    def _extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """Extraire l'auteur de l'article"""
        # Meta tags
        meta_author = soup.find('meta', attrs={'name': 'author'})
        if meta_author and meta_author.get('content'):
            return meta_author['content']
        
        # Sélecteurs courants
        selectors = [
            '.author-name',
            '.author',
            '.by-author',
            'span.author',
            'a[rel="author"]',
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                author = elem.get_text(strip=True)
                if author and len(author) < 100:
                    return author
        
        return None
    
    def _extract_image(self, soup: BeautifulSoup) -> Optional[str]:
        """Extraire l'image principale de l'article"""
        # Meta tags Open Graph
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
        
        # Image dans l'article
        selectors = [
            'article img',
            '.entry-content img',
            '.post-thumbnail img',
            '.featured-image img',
        ]
        
        for selector in selectors:
            img = soup.select_one(selector)
            if img and img.get('src'):
                return urljoin(self.base_url, img['src'])
        
        return None
    
    def scrape(self, media_id: int, days: int = 30, max_articles: int = 100) -> List[Article]:
        """
        Scraper le site complet
        
        Args:
            media_id: ID du média
            days: Nombre de jours à récupérer
            max_articles: Nombre maximum d'articles
        
        Returns:
            Liste d'articles
        """
        print(f"🌐 Scraping HTML depuis {self.base_url}...")
        
        # Date limite
        date_limit = datetime.now() - timedelta(days=days)
        
        # Récupérer la page d'accueil
        soup = self.get_page(self.base_url)
        if not soup:
            return []
        
        # Trouver les liens d'articles
        article_links = self.find_article_links(soup, max_links=max_articles)
        
        if not article_links:
            print("   ⚠️ Aucun lien d'article trouvé")
            return []
        
        # Scraper chaque article
        articles = []
        for i, url in enumerate(article_links, 1):
            print(f"   Article {i}/{len(article_links)}: {url[:80]}...")
            
            article = self.scrape_article(url, media_id, date_limit)
            if article:
                articles.append(article)
            
            # Pause pour ne pas surcharger le serveur
            time.sleep(0.5)
        
        print(f"✅ {len(articles)} articles scrapés avec succès")
        return articles
