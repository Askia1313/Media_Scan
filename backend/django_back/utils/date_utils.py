"""
Utilitaires pour la gestion des dates
"""

import re
from datetime import datetime, timedelta
from typing import Optional


def parse_french_date(date_str: str) -> Optional[datetime]:
    """
    Parser une date en français
    
    Args:
        date_str: Chaîne de date (ex: "15 novembre 2024")
    
    Returns:
        Objet datetime ou None
    """
    if not date_str:
        return None
    
    # Mapping des mois français
    months = {
        'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
        'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
        'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
    }
    
    # Pattern: "15 novembre 2024"
    pattern = r'(\d{1,2})\s+(\w+)\s+(\d{4})'
    match = re.search(pattern, date_str.lower())
    
    if match:
        day = int(match.group(1))
        month_name = match.group(2)
        year = int(match.group(3))
        
        month = months.get(month_name)
        if month:
            try:
                return datetime(year, month, day)
            except ValueError:
                pass
    
    return None


def is_within_days(date: datetime, days: int = 30) -> bool:
    """
    Vérifier si une date est dans les X derniers jours
    
    Args:
        date: Date à vérifier
        days: Nombre de jours
    
    Returns:
        True si dans la période
    """
    if not date:
        return False
    
    cutoff = datetime.now() - timedelta(days=days)
    return date >= cutoff


def format_relative_date(date: datetime) -> str:
    """
    Formater une date de manière relative (ex: "il y a 2 jours")
    
    Args:
        date: Date à formater
    
    Returns:
        Chaîne formatée
    """
    if not date:
        return "Date inconnue"
    
    now = datetime.now()
    diff = now - date
    
    if diff.days == 0:
        if diff.seconds < 3600:
            minutes = diff.seconds // 60
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
        else:
            hours = diff.seconds // 3600
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"
    elif diff.days == 1:
        return "hier"
    elif diff.days < 7:
        return f"il y a {diff.days} jours"
    elif diff.days < 30:
        weeks = diff.days // 7
        return f"il y a {weeks} semaine{'s' if weeks > 1 else ''}"
    else:
        months = diff.days // 30
        return f"il y a {months} mois"
