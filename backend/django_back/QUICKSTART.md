# ⚡ Quick Start - MÉDIA-SCAN

## 🚀 Démarrage Rapide (5 minutes)

### 1. Vérifier les Dépendances

```bash
# Les dépendances sont déjà installées dans votre environnement
# Vérification :
python -c "import requests, bs4, lxml; print('✅ Dépendances OK')"
```

### 2. Configurer les Sites

Éditez `sites.txt` :

```txt
https://lefaso.net
https://www.sidwaya.info
https://www.fasopresse.net
https://www.lobservateur.bf
https://www.aib.media
```

### 3. Lancer le Premier Scraping

```bash
python run_scraper.py
```

**C'est tout ! 🎉**

---

## 📊 Résultat Attendu

```
============================================================
🚀 MÉDIA-SCAN - Collecte Multi-Sites
============================================================

📋 5 sites à scraper
📅 Période: 30 derniers jours

[1/5] Traitement de https://lefaso.net...
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
```

---

## 🎯 Commandes Essentielles

```bash
# Scraping standard (30 jours)
python run_scraper.py

# Scraping 7 derniers jours
python run_scraper.py --days 7

# Scraper un seul site
python run_scraper.py --url https://lefaso.net

# Voir les statistiques
python run_scraper.py --stats

# Lancer les tests
python test_scraper.py
```

---

## 📁 Fichiers Créés

Après le premier scraping :

```
django_back/
├── data/
│   └── media_scan.db       # Base de données SQLite (créée auto)
│
├── sites.txt               # Votre configuration
├── run_scraper.py          # Script principal
└── test_scraper.py         # Tests
```

---

## 🔍 Visualiser les Données

### Option 1 : Python

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

# Statistiques
stats = db.get_scraping_stats()
print(f"Total articles: {stats['total_articles']}")

# Articles récents
articles = db.get_recent_articles(days=7, limit=10)
for article in articles:
    print(f"- {article.titre}")
```

### Option 2 : SQLite Browser

1. Téléchargez [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Ouvrez `data/media_scan.db`
3. Explorez les tables

### Option 3 : Ligne de Commande

```bash
# Afficher les stats
python run_scraper.py --stats
```

---

## 🎓 Exemples d'Utilisation

### Scraping Quotidien

```bash
# Récupérer seulement les nouveaux articles (1 jour)
python run_scraper.py --days 1
```

### Analyse Historique

```bash
# Récupérer 60 jours d'articles
python run_scraper.py --days 60
```

### Test d'un Nouveau Site

```bash
# Tester avant d'ajouter à sites.txt
python run_scraper.py --url https://nouveau-site.bf
```

---

## ✅ Vérification du Système

### Test Complet

```bash
python test_scraper.py
```

**Résultat attendu :**
```
============================================================
🧪 TESTS DU SYSTÈME DE SCRAPING
============================================================

============================================================
TEST 1: Détection WordPress
============================================================

🔍 Test: https://lefaso.net
   ✅ WordPress détecté

🔍 Test: https://www.sidwaya.info
   ✅ WordPress détecté

============================================================
TEST 2: Scraping WordPress
============================================================

📡 Test scraping: https://lefaso.net
✅ 145 articles récupérés
💾 145 articles sauvegardés en base de données

============================================================
✅ TESTS TERMINÉS
============================================================
```

---

## 🐛 Problèmes Courants

### "ModuleNotFoundError: No module named 'requests'"

```bash
pip install requests beautifulsoup4 lxml
```

### "Site non WordPress ou API non accessible"

**Normal** : Le système bascule automatiquement sur HTML scraping.

### "Aucun article trouvé"

**Vérifiez :**
1. Connexion internet
2. URL correcte dans `sites.txt`
3. Site accessible dans un navigateur

---

## 📚 Documentation Complète

- **README_SCRAPING.md** : Documentation détaillée
- **GUIDE_UTILISATION.md** : Guide d'utilisation
- **ARCHITECTURE.md** : Architecture technique

---

## 🎯 Prochaines Étapes

1. ✅ Scraper les médias burkinabè
2. 🔄 Automatiser le scraping quotidien
3. 📊 Développer le dashboard de visualisation
4. 🤖 Ajouter la classification ML
5. 🔍 Implémenter la détection de contenus sensibles

---

## 💡 Conseils

- **Scrapez régulièrement** : Tous les jours avec `--days 1`
- **Vérifiez les stats** : `python run_scraper.py --stats`
- **Testez d'abord** : Utilisez `--url` pour tester un nouveau site
- **Soyez patient** : Le scraping HTML prend du temps (pauses automatiques)

---

## 🚀 Vous êtes Prêt !

```bash
# Lancez votre premier scraping maintenant :
python run_scraper.py
```

**Bonne collecte ! 📰**
