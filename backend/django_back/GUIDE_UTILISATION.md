# 🚀 Guide d'Utilisation Rapide - MÉDIA-SCAN

## 📝 Configuration Initiale

### 1. Configurer les sites à scraper

Éditez le fichier `sites.txt` et ajoutez les URLs des médias :

```txt
https://lefaso.net
https://www.sidwaya.info
https://www.fasopresse.net
https://www.lobservateur.bf
https://www.aib.media
```

### 2. Vérifier les dépendances

```bash
pip install requests beautifulsoup4 lxml
```

---

## 🎯 Utilisation Basique

### Scraper tous les sites (30 derniers jours)

```bash
python run_scraper.py
```

### Scraper avec une période personnalisée

```bash
# 7 derniers jours
python run_scraper.py --days 7

# 60 derniers jours
python run_scraper.py --days 60
```

### Scraper un seul site

```bash
python run_scraper.py --url https://lefaso.net
```

### Afficher les statistiques

```bash
python run_scraper.py --stats
```

---

## 🧪 Tester le Système

### Lancer les tests

```bash
python test_scraper.py
```

**Tests effectués :**
1. ✅ Détection WordPress sur plusieurs sites
2. ✅ Scraping WordPress avec API
3. ✅ Scraping HTML (fallback)
4. ✅ Sauvegarde en base de données
5. ✅ Statistiques

---

## 📊 Comprendre les Résultats

### Sortie du scraping

```
============================================================
🎯 Scraping: Lefaso (https://lefaso.net)
============================================================

📡 Tentative 1: API WordPress...
✅ Site WordPress détecté!
📡 Récupération articles WordPress depuis https://lefaso.net...
   Page 1: 100 articles récupérés
   Page 2: 45 articles récupérés
✅ Total: 145 articles récupérés
✅ 145 articles collectés via API WordPress
```

**Signification :**
- ✅ **WordPress détecté** : Le site utilise WordPress, données de qualité
- 📡 **Pages récupérées** : Nombre de pages d'articles scrapées
- ✅ **Total** : Nombre total d'articles collectés

### Méthodes de scraping

| Méthode | Description | Qualité |
|---------|-------------|---------|
| `wordpress_api` | API WordPress REST | ⭐⭐⭐⭐⭐ Excellente |
| `html_scraping` | Scraping HTML générique | ⭐⭐⭐ Bonne |
| `error` | Échec du scraping | ❌ Aucune donnée |

---

## 🗄️ Accéder aux Données

### Base de données SQLite

Les données sont sauvegardées dans `data/media_scan.db`

### Visualiser avec Python

```python
from database.db_manager import DatabaseManager

# Initialiser
db = DatabaseManager()

# Récupérer les articles récents
articles = db.get_recent_articles(days=30, limit=10)

for article in articles:
    print(f"{article.titre}")
    print(f"URL: {article.url}")
    print(f"Date: {article.date_publication}")
    print(f"Contenu: {article.contenu[:200]}...")
    print("-" * 60)
```

### Visualiser avec SQLite Browser

1. Téléchargez [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Ouvrez `data/media_scan.db`
3. Explorez les tables `articles` et `medias`

---

## 🔧 Personnalisation

### Modifier la période de collecte

Dans `run_scraper.py`, changez la valeur par défaut :

```python
parser.add_argument(
    '--days',
    type=int,
    default=30,  # Changez ici
    help='Nombre de jours à récupérer'
)
```

### Ajouter un nouveau site

1. Ajoutez l'URL dans `sites.txt`
2. Lancez : `python run_scraper.py`

Le système détecte automatiquement WordPress ou utilise HTML.

### Modifier les sélecteurs HTML

Si un site spécifique ne fonctionne pas, éditez `scrapers/html_scraper.py` :

```python
def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
    selectors = [
        'h1.mon-selecteur-custom',  # Ajoutez ici
        'h1.entry-title',
        # ...
    ]
```

---

## 📈 Automatisation

### Scraping quotidien (Windows)

Créez un fichier `scrape_daily.bat` :

```batch
@echo off
cd C:\Users\DarkSide\Desktop\Media_Scanne\backend\django_back
python run_scraper.py --days 1
```

Ajoutez-le au Planificateur de tâches Windows pour l'exécuter tous les jours.

### Scraping quotidien (Linux/Mac)

Ajoutez au crontab :

```bash
# Tous les jours à 6h du matin
0 6 * * * cd /path/to/django_back && python run_scraper.py --days 1
```

---

## 🐛 Résolution de Problèmes

### "Site non WordPress ou API non accessible"

**Normal** : Le système bascule automatiquement sur HTML scraping.

### "Aucun article trouvé"

**Vérifiez :**
1. Connexion internet
2. URL correcte dans `sites.txt`
3. Site accessible dans un navigateur

**Solution :** Testez avec un seul site :
```bash
python run_scraper.py --url https://lefaso.net
```

### "Database is locked"

**Cause :** Un autre processus utilise la base de données.

**Solution :** Attendez la fin du scraping en cours.

### Erreur de parsing HTML

**Cause :** Structure HTML du site non reconnue.

**Solution :** Modifiez les sélecteurs dans `scrapers/html_scraper.py`

---

## 💡 Conseils

### Performance

- ✅ Scrapez régulièrement (ex: tous les jours) plutôt que tout d'un coup
- ✅ Limitez la période avec `--days` pour aller plus vite
- ✅ Le système inclut des pauses automatiques pour ne pas surcharger les serveurs

### Qualité des données

- ⭐ **WordPress API** : Données structurées, complètes et fiables
- ⭐ **HTML Scraping** : Données moins structurées, peut nécessiter des ajustements

### Stockage

- La base de données SQLite est légère (~1 Mo pour 1000 articles)
- Nettoyez les anciens articles si nécessaire :

```python
from database.db_manager import DatabaseManager
db = DatabaseManager()
db.clear_old_articles(days=90)  # Supprimer articles > 90 jours
```

---

## 📞 Commandes Utiles

```bash
# Scraping standard
python run_scraper.py

# Scraping avec période personnalisée
python run_scraper.py --days 7

# Scraper un seul site
python run_scraper.py --url https://lefaso.net

# Statistiques
python run_scraper.py --stats

# Tests
python test_scraper.py

# Aide
python run_scraper.py --help
```

---

## ✅ Checklist de Vérification

Avant de lancer le scraping :

- [ ] Python 3.9+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichier `sites.txt` configuré avec les URLs
- [ ] Connexion internet active
- [ ] Tests réussis (`python test_scraper.py`)

**Prêt à scraper ! 🚀**
