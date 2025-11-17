"""
Modèles de données pour les articles et médias
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Media:
    """Modèle pour un média"""
    id: Optional[int] = None
    nom: str = ""
    url: str = ""
    type_site: str = ""  # wordpress, html, autre
    facebook_page: Optional[str] = None  # Nom/ID de la page Facebook
    twitter_account: Optional[str] = None  # Nom du compte Twitter (sans @)
    actif: bool = True
    derniere_collecte: Optional[datetime] = None
    created_at: Optional[datetime] = None


@dataclass
class Article:
    """Modèle pour un article"""
    id: Optional[int] = None
    media_id: int = 0
    titre: str = ""
    contenu: str = ""
    extrait: str = ""
    url: str = ""
    auteur: Optional[str] = None
    date_publication: Optional[datetime] = None
    image_url: Optional[str] = None
    categories: Optional[str] = None  # JSON string
    tags: Optional[str] = None  # JSON string
    
    # Métadonnées de scraping
    source_type: str = ""  # wordpress_api, html_scraping
    scraped_at: Optional[datetime] = None
    
    # Engagement (si disponible)
    vues: int = 0
    commentaires: int = 0
    
    created_at: Optional[datetime] = None
