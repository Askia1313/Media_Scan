"""
Utilitaires pour le traitement de texte
"""

import re
from typing import List


def clean_text(text: str) -> str:
    """
    Nettoyer un texte
    
    Args:
        text: Texte à nettoyer
    
    Returns:
        Texte nettoyé
    """
    if not text:
        return ""
    
    # Supprimer les espaces multiples
    text = re.sub(r'\s+', ' ', text)
    
    # Supprimer les caractères spéciaux problématiques
    text = text.replace('\xa0', ' ')  # Non-breaking space
    text = text.replace('\u200b', '')  # Zero-width space
    
    # Trim
    text = text.strip()
    
    return text


def truncate_text(text: str, max_length: int = 300, suffix: str = '...') -> str:
    """
    Tronquer un texte à une longueur maximale
    
    Args:
        text: Texte à tronquer
        max_length: Longueur maximale
        suffix: Suffixe à ajouter si tronqué
    
    Returns:
        Texte tronqué
    """
    if not text or len(text) <= max_length:
        return text
    
    # Tronquer au dernier espace avant max_length
    truncated = text[:max_length].rsplit(' ', 1)[0]
    return truncated + suffix


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extraire des mots-clés simples d'un texte
    
    Args:
        text: Texte source
        max_keywords: Nombre maximum de mots-clés
    
    Returns:
        Liste de mots-clés
    """
    if not text:
        return []
    
    # Convertir en minuscules
    text = text.lower()
    
    # Supprimer la ponctuation
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Mots vides français
    stopwords = {
        'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou', 'mais',
        'donc', 'or', 'ni', 'car', 'ce', 'cette', 'ces', 'mon', 'ton', 'son',
        'ma', 'ta', 'sa', 'mes', 'tes', 'ses', 'notre', 'votre', 'leur',
        'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
        'qui', 'que', 'quoi', 'dont', 'où', 'est', 'sont', 'a', 'ont',
        'dans', 'sur', 'sous', 'avec', 'sans', 'pour', 'par', 'en'
    }
    
    # Extraire les mots
    words = text.split()
    
    # Filtrer et compter
    word_freq = {}
    for word in words:
        if len(word) > 3 and word not in stopwords:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Trier par fréquence
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Retourner les N premiers
    return [word for word, freq in sorted_words[:max_keywords]]


def remove_html_tags(text: str) -> str:
    """
    Supprimer les balises HTML d'un texte
    
    Args:
        text: Texte avec HTML
    
    Returns:
        Texte sans HTML
    """
    if not text:
        return ""
    
    # Supprimer les balises
    clean = re.sub(r'<[^>]+>', '', text)
    
    # Nettoyer les espaces
    clean = clean_text(clean)
    
    return clean
