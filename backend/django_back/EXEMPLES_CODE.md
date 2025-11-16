# 💻 Exemples de Code - MÉDIA-SCAN

## 📋 Table des Matières

1. [Utilisation Basique](#utilisation-basique)
2. [Scraping Personnalisé](#scraping-personnalisé)
3. [Accès aux Données](#accès-aux-données)
4. [Statistiques](#statistiques)
5. [Automatisation](#automatisation)

---

## 🚀 Utilisation Basique

### Scraper Tous les Sites

```python
from database.db_manager import DatabaseManager
from scrapers.scraper_manager import ScraperManager

# Initialiser
db = DatabaseManager()
manager = ScraperManager(db)

# Scraper tous les sites du fichier sites.txt
stats = manager.scrape_all_sites(
    sites_file='sites.txt',
    days=30  # 30 derniers jours
)

print(f"Total articles collectés: {stats['total_articles']}")
```

### Scraper un Seul Site

```python
from database.db_manager import DatabaseManager
from scrapers.scraper_manager import ScraperManager

db = DatabaseManager()
manager = ScraperManager(db)

# Scraper Lefaso.net
count, method, message = manager.scrape_site(
    url='https://lefaso.net',
    days=30
)

print(f"Méthode: {method}")
print(f"Articles: {count}")
print(message)
```

---

## 🔧 Scraping Personnalisé

### WordPress API Directement

```python
from database.db_manager import DatabaseManager
from scrapers.wordpress_scraper import WordPressScraper

db = DatabaseManager()

# Créer le scraper
scraper = WordPressScraper('https://lefaso.net')

# Vérifier si c'est WordPress
if scraper.is_wordpress():
    print("✅ WordPress détecté")
    
    # Ajouter le média
    media_id = db.add_media('Lefaso.net', 'https://lefaso.net', 'wordpress')
    
    # Scraper
    articles = scraper.scrape(media_id, days=30)
    
    # Sauvegarder
    for article in articles:
        db.add_article(article)
    
    print(f"✅ {len(articles)} articles collectés")
else:
    print("❌ Pas WordPress")
```

### HTML Scraping Directement

```python
from database.db_manager import DatabaseManager
from scrapers.html_scraper import HTMLScraper

db = DatabaseManager()

# Créer le scraper
scraper = HTMLScraper('https://www.aib.media')

# Ajouter le média
media_id = db.add_media('AIB', 'https://www.aib.media', 'html')

# Scraper (max 20 articles)
articles = scraper.scrape(media_id, days=30, max_articles=20)

# Sauvegarder
for article in articles:
    db.add_article(article)

print(f"✅ {len(articles)} articles collectés")
```

---

## 📊 Accès aux Données

### Récupérer les Articles Récents

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

# Articles des 7 derniers jours
articles = db.get_recent_articles(days=7, limit=50)

for article in articles:
    print(f"Titre: {article.titre}")
    print(f"Média: {article.media_id}")
    print(f"Date: {article.date_publication}")
    print(f"URL: {article.url}")
    print(f"Contenu: {article.contenu[:200]}...")
    print("-" * 60)
```

### Récupérer les Articles d'un Média

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

# Récupérer le média
media = db.get_media_by_url('https://lefaso.net')

if media:
    # Articles de ce média
    articles = db.get_articles_by_media(media.id, limit=100)
    
    print(f"📰 {len(articles)} articles de {media.nom}")
    
    for article in articles:
        print(f"- {article.titre}")
```

### Vérifier si un Article Existe

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

url = "https://lefaso.net/spip.php?article123456"

if db.article_exists(url):
    print("✅ Article déjà en base")
else:
    print("❌ Article non trouvé")
```

---

## 📈 Statistiques

### Statistiques Globales

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

stats = db.get_scraping_stats()

print(f"📰 Total articles: {stats['total_articles']}")
print(f"\n📺 Articles par média:")
for media, count in stats['articles_par_media'].items():
    print(f"   • {media}: {count} articles")

print(f"\n🔧 Articles par source:")
for source, count in stats['articles_par_source'].items():
    print(f"   • {source}: {count} articles")

print(f"\n📋 Derniers logs:")
for log in stats['derniers_logs'][:5]:
    print(f"   • {log['media_nom']}: {log['articles_collectes']} articles ({log['status']})")
```

### Compter les Articles

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

# Total
total = db.get_article_count()
print(f"Total articles: {total}")

# Par média
media = db.get_media_by_url('https://lefaso.net')
if media:
    count = db.get_article_count(media_id=media.id)
    print(f"Articles de {media.nom}: {count}")
```

### Tous les Médias Actifs

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

medias = db.get_all_active_medias()

print(f"📺 {len(medias)} médias actifs:")
for media in medias:
    print(f"   • {media.nom} ({media.type_site})")
    print(f"     URL: {media.url}")
    print(f"     Dernière collecte: {media.derniere_collecte}")
```

---

## 🤖 Automatisation

### Script de Scraping Quotidien

```python
#!/usr/bin/env python3
# scrape_daily.py

from database.db_manager import DatabaseManager
from scrapers.scraper_manager import ScraperManager
from datetime import datetime

def main():
    print(f"🚀 Scraping quotidien - {datetime.now()}")
    
    # Initialiser
    db = DatabaseManager()
    manager = ScraperManager(db)
    
    # Scraper seulement les nouveaux articles (1 jour)
    stats = manager.scrape_all_sites(
        sites_file='sites.txt',
        days=1
    )
    
    print(f"\n✅ {stats['total_articles']} nouveaux articles collectés")
    
    # Envoyer un email de rapport (optionnel)
    # send_report_email(stats)

if __name__ == '__main__':
    main()
```

**Automatisation Windows (Planificateur de tâches) :**

```batch
@echo off
cd C:\Users\DarkSide\Desktop\Media_Scanne\backend\django_back
python scrape_daily.py >> logs\scraping.log 2>&1
```

**Automatisation Linux/Mac (crontab) :**

```bash
# Tous les jours à 6h du matin
0 6 * * * cd /path/to/django_back && python scrape_daily.py >> logs/scraping.log 2>&1
```

### Nettoyage Automatique des Anciens Articles

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

# Supprimer les articles de plus de 90 jours
deleted = db.clear_old_articles(days=90)
print(f"🗑️ {deleted} anciens articles supprimés")

# Optimiser la base de données
db.vacuum()
print("✅ Base de données optimisée")
```

---

## 🔍 Recherche et Filtrage

### Recherche par Mot-Clé (Simple)

```python
from database.db_manager import DatabaseManager
import sqlite3

db = DatabaseManager()
conn = db.get_connection()
cursor = conn.cursor()

# Recherche dans le titre ou le contenu
keyword = "politique"

cursor.execute("""
    SELECT titre, url, date_publication
    FROM articles
    WHERE titre LIKE ? OR contenu LIKE ?
    ORDER BY date_publication DESC
    LIMIT 20
""", (f'%{keyword}%', f'%{keyword}%'))

results = cursor.fetchall()

print(f"🔍 {len(results)} articles trouvés pour '{keyword}':")
for titre, url, date in results:
    print(f"   • {titre}")
    print(f"     {url}")
    print(f"     {date}")
    print()

conn.close()
```

### Filtrer par Catégorie

```python
from database.db_manager import DatabaseManager
import sqlite3
import json

db = DatabaseManager()
conn = db.get_connection()
cursor = conn.cursor()

# Articles de la catégorie "Politique"
cursor.execute("""
    SELECT titre, url, categories
    FROM articles
    WHERE categories LIKE '%Politique%'
    ORDER BY date_publication DESC
    LIMIT 20
""")

results = cursor.fetchall()

print(f"📰 {len(results)} articles de catégorie 'Politique':")
for titre, url, categories in results:
    print(f"   • {titre}")
    print(f"     Catégories: {categories}")
    print()

conn.close()
```

---

## 📤 Export de Données

### Export CSV

```python
from database.db_manager import DatabaseManager
import csv

db = DatabaseManager()

# Récupérer les articles
articles = db.get_recent_articles(days=30, limit=1000)

# Export CSV
with open('articles_export.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # En-têtes
    writer.writerow(['Titre', 'URL', 'Date', 'Auteur', 'Source'])
    
    # Données
    for article in articles:
        writer.writerow([
            article.titre,
            article.url,
            article.date_publication,
            article.auteur or '',
            article.source_type
        ])

print("✅ Export CSV terminé: articles_export.csv")
```

### Export JSON

```python
from database.db_manager import DatabaseManager
import json

db = DatabaseManager()

# Récupérer les articles
articles = db.get_recent_articles(days=30, limit=1000)

# Convertir en dictionnaires
articles_dict = []
for article in articles:
    articles_dict.append({
        'titre': article.titre,
        'url': article.url,
        'date_publication': str(article.date_publication),
        'auteur': article.auteur,
        'contenu': article.contenu,
        'source_type': article.source_type
    })

# Export JSON
with open('articles_export.json', 'w', encoding='utf-8') as f:
    json.dump(articles_dict, f, ensure_ascii=False, indent=2)

print("✅ Export JSON terminé: articles_export.json")
```

---

## 🧪 Tests et Validation

### Tester un Site Avant de l'Ajouter

```python
from scrapers.wordpress_scraper import WordPressScraper
from scrapers.html_scraper import HTMLScraper

url = "https://nouveau-site.bf"

# Test WordPress
print(f"🔍 Test de {url}...")
wp_scraper = WordPressScraper(url)

if wp_scraper.is_wordpress():
    print("✅ WordPress détecté - Recommandé")
else:
    print("⚠️ WordPress non détecté - HTML scraping sera utilisé")
    
    # Test HTML
    html_scraper = HTMLScraper(url)
    soup = html_scraper.get_page(url)
    
    if soup:
        links = html_scraper.find_article_links(soup)
        print(f"   {len(links)} liens d'articles trouvés")
        
        if len(links) > 0:
            print("✅ HTML scraping possible")
        else:
            print("❌ Aucun article trouvé - Structure HTML non compatible")
    else:
        print("❌ Impossible de récupérer la page")
```

### Valider les Données Collectées

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

# Vérifier les articles sans contenu
conn = db.get_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT COUNT(*) as count
    FROM articles
    WHERE contenu IS NULL OR LENGTH(contenu) < 100
""")

invalid_count = cursor.fetchone()['count']

if invalid_count > 0:
    print(f"⚠️ {invalid_count} articles avec contenu invalide")
else:
    print("✅ Tous les articles ont un contenu valide")

conn.close()
```

---

## 🎨 Personnalisation

### Ajouter un Nouveau Scraper

```python
# scrapers/custom_scraper.py

from typing import List
from database.models import Article
from datetime import datetime

class CustomScraper:
    """Scraper personnalisé pour un site spécifique"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def scrape(self, media_id: int, days: int = 30) -> List[Article]:
        """
        Scraper personnalisé
        
        Returns:
            Liste d'objets Article
        """
        articles = []
        
        # Votre logique de scraping ici
        # ...
        
        return articles
```

### Modifier les Sélecteurs HTML

```python
# Dans scrapers/html_scraper.py

def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
    # Ajouter vos sélecteurs personnalisés
    selectors = [
        'h1.mon-selecteur-custom',  # Votre sélecteur
        'h1.entry-title',
        'h1.post-title',
        # ...
    ]
    
    for selector in selectors:
        elem = soup.select_one(selector)
        if elem:
            return elem.get_text(strip=True)
    
    return None
```

---

## 💡 Conseils et Bonnes Pratiques

### 1. Gestion des Erreurs

```python
from database.db_manager import DatabaseManager
from scrapers.scraper_manager import ScraperManager

db = DatabaseManager()
manager = ScraperManager(db)

try:
    count, method, message = manager.scrape_site('https://lefaso.net', days=30)
    print(f"✅ Succès: {count} articles")
except Exception as e:
    print(f"❌ Erreur: {e}")
    # Logger l'erreur
    import traceback
    traceback.print_exc()
```

### 2. Scraping Progressif

```python
# Scraper par petits lots pour éviter les timeouts
urls = [
    'https://lefaso.net',
    'https://www.sidwaya.info',
    'https://www.fasopresse.net',
    # ...
]

for url in urls:
    try:
        print(f"\n🎯 Scraping {url}...")
        count, method, message = manager.scrape_site(url, days=7)
        print(message)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        continue  # Continuer avec le site suivant
```

### 3. Monitoring

```python
from database.db_manager import DatabaseManager
from datetime import datetime

db = DatabaseManager()

# Vérifier la dernière collecte de chaque média
medias = db.get_all_active_medias()

print("📊 État des médias:")
for media in medias:
    if media.derniere_collecte:
        print(f"   • {media.nom}: {media.derniere_collecte}")
    else:
        print(f"   • {media.nom}: ❌ Jamais scrapé")
```

---

## 🎯 Cas d'Usage Avancés

### Dashboard Simple en Console

```python
from database.db_manager import DatabaseManager
from datetime import datetime

def show_dashboard():
    db = DatabaseManager()
    stats = db.get_scraping_stats()
    
    print("\n" + "="*60)
    print("📊 MÉDIA-SCAN DASHBOARD")
    print("="*60)
    print(f"\n📰 Total articles: {stats['total_articles']}")
    
    print(f"\n📺 Top 5 médias:")
    sorted_medias = sorted(
        stats['articles_par_media'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    for i, (media, count) in enumerate(sorted_medias[:5], 1):
        print(f"   {i}. {media}: {count} articles")
    
    print(f"\n🔧 Méthodes de scraping:")
    for method, count in stats['articles_par_source'].items():
        print(f"   • {method}: {count} articles")
    
    print(f"\n📅 Dernière mise à jour: {datetime.now()}")
    print("="*60)

if __name__ == '__main__':
    show_dashboard()
```

---

**Pour plus d'exemples, consultez les scripts `run_scraper.py` et `test_scraper.py` !**
