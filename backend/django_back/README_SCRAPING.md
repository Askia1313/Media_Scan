# 📰 MÉDIA-SCAN - Système de Scraping Intelligent

## 🎯 Vue d'Ensemble

Système de scraping automatique pour collecter les articles des médias burkinabè avec :
- ✅ **Détection automatique WordPress** (API REST)
- ✅ **Fallback HTML** si WordPress non disponible
- ✅ **Sauvegarde SQLite** avec gestion des doublons
- ✅ **Collecte des 30 derniers jours**
- ✅ **Multi-sites** via fichier de configuration

---

## 🏗️ Architecture

```
django_back/
├── database/
│   ├── __init__.py
│   ├── models.py           # Modèles Article et Media
│   ├── schema.sql          # Schéma SQLite
│   └── db_manager.py       # Gestionnaire de base de données
│
├── scrapers/
│   ├── __init__.py
│   ├── wordpress_scraper.py    # Scraper WordPress API
│   ├── html_scraper.py         # Scraper HTML (fallback)
│   └── scraper_manager.py      # Gestionnaire principal
│
├── utils/
│   ├── __init__.py
│   ├── text_utils.py       # Utilitaires texte
│   └── date_utils.py       # Utilitaires dates
│
├── data/
│   └── media_scan.db       # Base de données SQLite (créée auto)
│
├── sites.txt               # Liste des sites à scraper
├── run_scraper.py          # Script principal
├── test_scraper.py         # Script de test
└── requirements.txt        # Dépendances
```

---

## 📋 Fonctionnalités

### 1. Scraping WordPress (Priorité)

Le système détecte automatiquement si un site utilise WordPress et utilise l'API REST :

**Avantages :**
- ✅ Données structurées (titre, contenu, date, auteur, catégories, tags)
- ✅ Rapide et fiable
- ✅ Pas de parsing HTML complexe
- ✅ Métadonnées complètes

**Données récupérées :**
- Titre de l'article
- Contenu complet (texte)
- Extrait
- URL
- Auteur
- Date de publication
- Image à la une
- Catégories
- Tags
- Nombre de commentaires

### 2. Scraping HTML (Fallback)

Si WordPress n'est pas disponible, le système bascule automatiquement sur le scraping HTML :

**Fonctionnement :**
- Récupération de la page d'accueil
- Détection automatique des liens d'articles
- Extraction du contenu via sélecteurs CSS génériques
- Parsing intelligent du titre, contenu, date, auteur

**Limitations :**
- Moins de métadonnées
- Dépend de la structure HTML du site
- Plus lent

### 3. Base de Données SQLite

**Tables :**
- `medias` : Liste des médias scrapés
- `articles` : Articles collectés
- `scraping_logs` : Logs de scraping

**Fonctionnalités :**
- Gestion automatique des doublons (par URL)
- Index pour performances
- Statistiques de collecte
- Nettoyage des anciens articles

---

## 🚀 Installation

### 1. Prérequis

```bash
Python 3.9+
```

### 2. Installer les dépendances

```bash
cd django_back
pip install -r requirements.txt
```

**Dépendances principales :**
- `requests` : Requêtes HTTP
- `beautifulsoup4` : Parsing HTML
- `lxml` : Parser XML/HTML rapide

---

## 📝 Configuration

### Fichier `sites.txt`

Créez ou modifiez le fichier `sites.txt` avec les URLs des sites à scraper :

```txt
# Médias burkinabè
https://lefaso.net
https://www.sidwaya.info
https://www.fasopresse.net
https://www.lobservateur.bf
https://www.aib.media

# Autres médias (décommentez si nécessaire)
# https://www.burkina24.com
# https://www.lepays.bf
```

**Format :**
- Une URL par ligne
- Les lignes commençant par `#` sont des commentaires
- Les lignes vides sont ignorées

---

## 🎮 Utilisation

### 1. Scraper tous les sites

```bash
python run_scraper.py
```

**Options :**
```bash
# Spécifier le nombre de jours
python run_scraper.py --days 30

# Utiliser un autre fichier de sites
python run_scraper.py --sites-file mes_sites.txt

# Spécifier le chemin de la base de données
python run_scraper.py --db-path data/custom.db
```

### 2. Scraper un seul site

```bash
python run_scraper.py --url https://lefaso.net
```

### 3. Afficher les statistiques

```bash
python run_scraper.py --stats
```

### 4. Tester le système

```bash
python test_scraper.py
```

**Tests effectués :**
1. Détection WordPress sur plusieurs sites
2. Scraping WordPress avec sauvegarde
3. Scraping HTML avec sauvegarde
4. Opérations de base de données

---

## 📊 Exemple de Sortie

```
============================================================
🚀 MÉDIA-SCAN - Collecte Multi-Sites
============================================================

📋 5 sites à scraper
📅 Période: 30 derniers jours

============================================================
🎯 Scraping: Lefaso (https://lefaso.net)
============================================================

📡 Tentative 1: API WordPress...
✅ Site WordPress détecté!
📡 Récupération articles WordPress depuis https://lefaso.net...
   Page 1: 100 articles récupérés
   Page 2: 100 articles récupérés
   Page 3: 45 articles récupérés
✅ Total: 245 articles récupérés
✅ 245 articles collectés via API WordPress

[2/5] Traitement de https://www.sidwaya.info...
...

============================================================
📊 RÉSUMÉ DE LA COLLECTE
============================================================

✅ Sites traités: 5
   • Succès: 4
   • Erreurs: 1

📰 Total articles collectés: 487

🔧 Par méthode:
   • WordPress API: 412 articles
   • HTML Scraping: 75 articles

📋 Détails par site:
   ✅ https://lefaso.net: 245 articles (wordpress_api)
   ✅ https://www.sidwaya.info: 167 articles (wordpress_api)
   ✅ https://www.fasopresse.net: 89 articles (html_scraping)
   ✅ https://www.aib.media: 56 articles (html_scraping)
   ❌ https://www.lobservateur.bf: 0 articles (error)
```

---

## 🔧 API Python

### Utilisation programmatique

```python
from database.db_manager import DatabaseManager
from scrapers.scraper_manager import ScraperManager

# Initialiser
db = DatabaseManager('data/media_scan.db')
manager = ScraperManager(db)

# Scraper un site
count, method, message = manager.scrape_site('https://lefaso.net', days=30)
print(f"Collecté: {count} articles via {method}")

# Scraper tous les sites
stats = manager.scrape_all_sites('sites.txt', days=30)
print(f"Total: {stats['total_articles']} articles")

# Récupérer les articles
articles = db.get_recent_articles(days=30, limit=100)
for article in articles:
    print(f"{article.titre} - {article.date_publication}")

# Statistiques
stats = db.get_scraping_stats()
print(f"Total articles: {stats['total_articles']}")
```

---

## 📦 Structure de Données

### Modèle Article

```python
@dataclass
class Article:
    id: Optional[int]
    media_id: int
    titre: str
    contenu: str
    extrait: str
    url: str
    auteur: Optional[str]
    date_publication: Optional[datetime]
    image_url: Optional[str]
    categories: Optional[str]  # JSON
    tags: Optional[str]  # JSON
    source_type: str  # 'wordpress_api' ou 'html_scraping'
    scraped_at: Optional[datetime]
    vues: int
    commentaires: int
```

### Modèle Media

```python
@dataclass
class Media:
    id: Optional[int]
    nom: str
    url: str
    type_site: str  # 'wordpress', 'html', 'unknown'
    actif: bool
    derniere_collecte: Optional[datetime]
```

---

## 🛠️ Personnalisation

### Ajouter un nouveau site

1. Ajoutez l'URL dans `sites.txt`
2. Lancez le scraper : `python run_scraper.py`

Le système détectera automatiquement la meilleure méthode.

### Modifier les sélecteurs HTML

Si le scraping HTML ne fonctionne pas pour un site spécifique, modifiez `scrapers/html_scraper.py` :

```python
def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
    # Ajoutez vos sélecteurs personnalisés
    selectors = [
        'h1.custom-title',  # Votre sélecteur
        'h1.entry-title',
        # ...
    ]
```

### Changer la période de collecte

```bash
# 7 derniers jours
python run_scraper.py --days 7

# 90 derniers jours
python run_scraper.py --days 90
```

---

## 🐛 Dépannage

### Erreur : "Site non WordPress ou API non accessible"

**Cause :** Le site n'utilise pas WordPress ou l'API est désactivée.

**Solution :** Le système bascule automatiquement sur le scraping HTML.

### Erreur : "Aucun article trouvé"

**Causes possibles :**
1. Le site a changé sa structure HTML
2. Le site bloque les scrapers
3. Problème de connexion

**Solutions :**
1. Vérifiez votre connexion internet
2. Testez manuellement l'URL dans un navigateur
3. Modifiez les sélecteurs CSS dans `html_scraper.py`

### Erreur : "Database locked"

**Cause :** Plusieurs processus accèdent à la base de données simultanément.

**Solution :** Attendez que le scraping en cours se termine.

### Articles dupliqués

**Impossible :** Le système utilise l'URL comme clé unique (contrainte UNIQUE).

---

## 📈 Performance

### Vitesse de scraping

- **WordPress API** : ~100 articles/minute
- **HTML Scraping** : ~10-20 articles/minute (avec pauses)

### Recommandations

1. **Pauses entre requêtes** : Le système inclut des pauses automatiques (1-2s)
2. **Limiter le nombre d'articles** : Utilisez `--days` pour limiter la période
3. **Scraping progressif** : Scrapez régulièrement (ex: tous les jours) plutôt que tout d'un coup

---

## 🔒 Considérations Légales

### Respect des sites

- ✅ Scraping de contenu public uniquement
- ✅ Pauses entre requêtes pour ne pas surcharger les serveurs
- ✅ User-Agent identifiable
- ✅ Respect du robots.txt (à implémenter si nécessaire)

### Utilisation des données

- Les données collectées sont à usage d'analyse et de recherche
- Respectez les droits d'auteur des contenus
- Ne republiez pas les contenus sans autorisation

---

## 🚀 Prochaines Étapes

### Améliorations possibles

1. **Respect du robots.txt** : Vérifier automatiquement
2. **Scraping incrémental** : Ne récupérer que les nouveaux articles
3. **Détection de langue** : Filtrer par langue française
4. **Classification automatique** : Catégoriser les articles (ML)
5. **API REST** : Exposer les données via API
6. **Dashboard** : Interface web pour visualiser les données
7. **Notifications** : Alertes pour nouveaux articles importants
8. **Export** : CSV, JSON, Excel

---

## 📞 Support

### Logs

Les logs de scraping sont sauvegardés dans la table `scraping_logs` :

```python
# Afficher les derniers logs
python run_scraper.py --stats
```

### Debug

Pour activer le mode debug, modifiez le code :

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📄 Licence

Ce projet est développé dans le cadre du Hackathon MTDPCE AI 2025.

---

## ✅ Checklist de Démarrage

- [ ] Python 3.9+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichier `sites.txt` configuré
- [ ] Tests exécutés (`python test_scraper.py`)
- [ ] Premier scraping lancé (`python run_scraper.py`)
- [ ] Statistiques vérifiées (`python run_scraper.py --stats`)

**Prêt à scraper ! 🚀**
