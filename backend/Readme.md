# 📰 Media Scanner - Backend API

API REST Django pour le scraping, l'analyse et la modération de contenus médiatiques burkinabè. Ce backend collecte automatiquement des articles de presse, posts Facebook et tweets, puis les analyse avec classification thématique et modération de contenu.

## 🏗️ Architecture

```
backend/
├── django_back/
│   ├── django_back/          # Configuration Django principale
│   │   ├── settings.py       # Configuration globale
│   │   ├── urls.py           # Routes principales + Swagger
│   │   └── wsgi.py           # Point d'entrée WSGI
│   │
│   ├── api/                  # Application API REST
│   │   ├── views.py          # Endpoints REST (médias, articles, stats, etc.)
│   │   ├── urls.py           # Routes API
│   │   ├── serializers.py    # Sérialiseurs DRF
│   │   ├── scheduler.py      # Automatisation du scraping
│   │   └── apps.py           # Configuration de l'app
│   │
│   ├── database/             # Gestion de la base de données
│   │   ├── db_manager.py     # Gestionnaire SQLite (CRUD)
│   │   ├── models.py         # Modèles de données (dataclasses)
│   │   └── schema.sql        # Schéma de base de données
│   │
│   ├── scrapers/             # Modules de scraping
│   │   ├── scraper_manager.py      # Gestionnaire principal
│   │   ├── rss_scraper.py          # Scraping RSS
│   │   ├── smart_html_scraper.py   # Scraping HTML intelligent
│   │   ├── facebook_scraper.py     # Scraping Facebook
│   │   └── twitter_scraper.py      # Scraping Twitter
│   │
│   ├── analysis/             # Modules d'analyse
│   │   ├── theme_classifier.py     # Classification thématique (Ollama + Mistral)
│   │   ├── audience_analyzer.py    # Analyse d'audience multi-plateformes
│   │   └── content_moderator.py    # Modération de contenu (toxicité, fake news)
│   │
│   ├── utils/                # Utilitaires
│   │   ├── date_utils.py     # Gestion des dates
│   │   └── text_utils.py     # Traitement de texte
│   │
│   ├── manage.py             # CLI Django
│   ├── requirements.txt      # Dépendances Python
│   ├── scrape_with_social.py # Script de scraping complet
│   ├── classify_articles.py  # Script de classification
│   ├── moderate_content.py   # Script de modération
│   └── show_audience.py      # Script d'analyse d'audience
│
└── data/
    └── media_scan.db         # Base de données SQLite
```

## 🛠️ Technologies

### Framework & API

- **Django 5.2.8** - Framework web Python
- **Django REST Framework 3.14.0** - API REST
- **drf-yasg 1.21.7** - Documentation Swagger/OpenAPI
- **django-cors-headers 4.3.1** - Gestion CORS

### Scraping & Parsing

- **requests 2.31.0** - Requêtes HTTP
- **beautifulsoup4 4.12.2** - Parsing HTML
- **feedparser 6.0.10** - Parsing RSS/Atom

### Base de données

- **SQLite 3** - Base de données embarquée

### IA & Analyse

- **Ollama + Mistral** - Classification thématique (externe)
- **Ollama + **Mistral****- Modération de contenu (externe)

### Utilitaires

- **python-dateutil 2.8.2** - Manipulation de dates
- **python-dotenv 1.0.0** - Variables d'environnement

## 📊 Base de données

### Schéma principal

#### Table `medias`

Stocke les médias à surveiller.

| Colonne               | Type      | Description                   |
| --------------------- | --------- | ----------------------------- |
| `id`                | INTEGER   | Clé primaire                 |
| `nom`               | TEXT      | Nom du média                 |
| `url`               | TEXT      | URL du site (unique)          |
| `type_site`         | TEXT      | Type : wordpress, html, autre |
| `facebook_page`     | TEXT      | Nom/ID de la page Facebook    |
| `twitter_account`   | TEXT      | Compte Twitter (sans @)       |
| `actif`             | BOOLEAN   | Média actif ou non           |
| `derniere_collecte` | TIMESTAMP | Date de dernière collecte    |
| `created_at`        | TIMESTAMP | Date de création             |

#### Table `articles`

Stocke les articles collectés.

| Colonne              | Type      | Description                  |
| -------------------- | --------- | ---------------------------- |
| `id`               | INTEGER   | Clé primaire                |
| `media_id`         | INTEGER   | Référence au média        |
| `titre`            | TEXT      | Titre de l'article           |
| `contenu`          | TEXT      | Contenu complet              |
| `extrait`          | TEXT      | Extrait/résumé             |
| `url`              | TEXT      | URL de l'article (unique)    |
| `auteur`           | TEXT      | Auteur                       |
| `date_publication` | TIMESTAMP | Date de publication          |
| `image_url`        | TEXT      | URL de l'image               |
| `categories`       | TEXT      | Catégories (JSON)           |
| `tags`             | TEXT      | Tags (JSON)                  |
| `source_type`      | TEXT      | wordpress_api, html_scraping |
| `vues`             | INTEGER   | Nombre de vues               |
| `commentaires`     | INTEGER   | Nombre de commentaires       |
| `scraped_at`       | TIMESTAMP | Date de scraping             |
| `created_at`       | TIMESTAMP | Date de création            |

#### Table `classifications`

Classifications thématiques des articles.

| Colonne           | Type      | Description                                                      |
| ----------------- | --------- | ---------------------------------------------------------------- |
| `id`            | INTEGER   | Clé primaire                                                    |
| `article_id`    | INTEGER   | Référence à l'article (unique)                                |
| `categorie`     | TEXT      | Politique, Économie, Sécurité, Santé, Culture, Sport, Autres |
| `confiance`     | REAL      | Score de confiance (0-1)                                         |
| `mots_cles`     | TEXT      | Mots-clés (JSON)                                                |
| `justification` | TEXT      | Explication de la classification                                 |
| `methode`       | TEXT      | mistral_ollama, keywords_fallback                                |
| `created_at`    | TIMESTAMP | Date de création                                                |

#### Table `facebook_posts`

Posts Facebook collectés.

| Colonne              | Type      | Description            |
| -------------------- | --------- | ---------------------- |
| `id`               | INTEGER   | Clé primaire          |
| `media_id`         | INTEGER   | Référence au média  |
| `post_id`          | TEXT      | ID Facebook (unique)   |
| `message`          | TEXT      | Contenu du post        |
| `url`              | TEXT      | URL du post            |
| `image_url`        | TEXT      | URL de l'image         |
| `date_publication` | TIMESTAMP | Date de publication    |
| `likes`            | INTEGER   | Nombre de likes        |
| `comments`         | INTEGER   | Nombre de commentaires |
| `shares`           | INTEGER   | Nombre de partages     |
| `engagement_total` | INTEGER   | Engagement total       |
| `scraped_at`       | TIMESTAMP | Date de scraping       |

#### Table `twitter_tweets`

Tweets collectés.

| Colonne              | Type      | Description           |
| -------------------- | --------- | --------------------- |
| `id`               | INTEGER   | Clé primaire         |
| `media_id`         | INTEGER   | Référence au média |
| `tweet_id`         | TEXT      | ID Twitter (unique)   |
| `text`             | TEXT      | Contenu du tweet      |
| `url`              | TEXT      | URL du tweet          |
| `image_url`        | TEXT      | URL de l'image        |
| `date_publication` | TIMESTAMP | Date de publication   |
| `retweets`         | INTEGER   | Nombre de retweets    |
| `replies`          | INTEGER   | Nombre de réponses   |
| `likes`            | INTEGER   | Nombre de likes       |
| `quotes`           | INTEGER   | Nombre de citations   |
| `impressions`      | INTEGER   | Nombre d'impressions  |
| `engagement_total` | INTEGER   | Engagement total      |
| `scraped_at`       | TIMESTAMP | Date de scraping      |

#### Table `content_moderation`

Analyses de modération de contenu.

| Colonne                  | Type      | Description                                 |
| ------------------------ | --------- | ------------------------------------------- |
| `id`                   | INTEGER   | Clé primaire                               |
| `content_type`         | TEXT      | article, facebook_post, tweet               |
| `content_id`           | INTEGER   | ID du contenu                               |
| `risk_score`           | REAL      | Score de risque (0-10)                      |
| `risk_level`           | TEXT      | MINIMAL, FAIBLE, MOYEN, ÉLEVÉ, CRITIQUE   |
| `should_flag`          | BOOLEAN   | Contenu à signaler                         |
| `is_toxic`             | BOOLEAN   | Contenu toxique                             |
| `toxicity_score`       | REAL      | Score de toxicité                          |
| `is_misinformation`    | BOOLEAN   | Désinformation détectée                  |
| `misinformation_score` | REAL      | Score de désinformation                    |
| `is_sensitive`         | BOOLEAN   | Contenu sensible                            |
| `sensitivity_score`    | REAL      | Score de sensibilité                       |
| `primary_issue`        | TEXT      | toxicity, misinformation, sensitivity, none |
| `analyzed_at`          | TIMESTAMP | Date d'analyse                              |
| `model_used`           | TEXT      | Modèle IA utilisé                         |

## 🔌 API REST

### Documentation interactive

- **Swagger UI** : `http://localhost:8000/swagger/`
- **ReDoc** : `http://localhost:8000/redoc/`
- **JSON Schema** : `http://localhost:8000/swagger.json`

### Endpoints principaux

#### 🏥 Health Check

```
GET /api/health/
```

Vérification de l'état du serveur.

#### 📰 Médias

```
GET    /api/medias/              # Liste tous les médias
GET    /api/medias/?actif=true   # Médias actifs uniquement
POST   /api/medias/              # Créer un nouveau média
GET    /api/medias/{id}/         # Détails d'un média
PUT    /api/medias/{id}/         # Mettre à jour un média
DELETE /api/medias/{id}/         # Supprimer un média
```

**Exemple de création de média :**

```json
POST /api/medias/
{
  "nom": "AIB",
  "url": "https://www.aib.media",
  "type_site": "wordpress",
  "facebook_page": "AIBBurkinaFaso",
  "twitter_account": "AibBurkina"
}
```

#### 📄 Articles

```
GET /api/articles/                    # Liste des articles récents
GET /api/articles/?media_id=1         # Articles d'un média
GET /api/articles/?days=7&limit=100   # Articles des 7 derniers jours
```

**Paramètres de requête :**

- `media_id` : Filtrer par média
- `days` : Nombre de jours (défaut: 7)
- `limit` : Nombre max de résultats (défaut: 100)

#### 🏷️ Classifications

```
GET /api/classifications/                      # Liste des classifications
GET /api/classifications/?categorie=Politique  # Par catégorie
GET /api/classifications/stats/?days=30        # Statistiques par catégorie
GET /api/classifications/weekly/?weeks=5       # Stats hebdomadaires
```

**Catégories disponibles :**

- Politique
- Économie
- Sécurité
- Santé
- Culture
- Sport
- Autres

#### 📘 Facebook

```
GET /api/facebook/posts/?media_id=1&limit=100
```

Liste des posts Facebook d'un média.

#### 🐦 Twitter

```
GET /api/twitter/tweets/?media_id=1&limit=100
```

Liste des tweets d'un média.

#### 👥 Audience

```
GET /api/audience/web/?days=30        # Audience Web (articles)
GET /api/audience/facebook/?days=30   # Audience Facebook
GET /api/audience/twitter/?days=30    # Audience Twitter
GET /api/audience/global/?days=30     # Audience globale combinée
GET /api/audience/inactive/?days_threshold=7  # Médias inactifs
```

#### 🏆 Classement

```
GET /api/ranking/?days=30
```

Classement des médias par engagement total.

#### 🔄 Scraping

```
POST /api/scraping/trigger/    # Déclencher un scraping manuel
GET  /api/scraping/schedule/   # Configuration du scraping automatique
PUT  /api/scraping/schedule/   # Modifier la configuration
GET  /api/scraping/history/    # Historique des tâches
```

**Exemple de déclenchement manuel :**

```json
POST /api/scraping/trigger/
{
  "all": true,
  "days": 7,
  "fb_posts": 10,
  "tweets": 10,
  "skip_facebook": false,
  "skip_twitter": false
}
```

**Configuration du scraping automatique :**

```json
PUT /api/scraping/schedule/
{
  "enabled": true,
  "frequency": "daily",
  "days": 7,
  "fb_posts": 10,
  "tweets": 10
}
```

**Fréquences disponibles :**

- `hourly` : Toutes les heures
- `daily` : Tous les jours
- `weekly` : Toutes les semaines

#### 🛡️ Modération

```
GET  /api/moderation/stats/          # Statistiques de modération
GET  /api/moderation/flagged/        # Contenus signalés
POST /api/moderation/content/        # Modérer un contenu
```

**Exemple de modération :**

```json
POST /api/moderation/content/
{
  "content_type": "article",
  "content_id": 123
}
```

#### 📊 Statistiques

```
GET /api/stats/
```

Vue d'ensemble des statistiques globales.

## 🚀 Installation

### Prérequis

- Python 3.10+
- SQLite 3
- Ollama (optionnel, pour classification et modération)

### Installation des dépendances

```bash
cd backend/django_back
pip install -r requirements.txt
```

### Configuration

1. **Créer le fichier [.env](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/backend/django_back/.env:0:0-0:0)** (optionnel) :

```bash
cp .env.example .env
```

2. **Variables d'environnement** ([.env](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/backend/django_back/.env:0:0-0:0)) :

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_PATH=../../data/media_scan.db
OLLAMA_URL=http://localhost:11434
```

### Lancement du serveur

```bash
python manage.py runserver
```

Le serveur démarre sur `http://localhost:8000/`

## 🔧 Utilisation

### Scripts CLI disponibles

#### 1. Scraping complet (Web + Social)

```bash
# Scraper tous les médias actifs
python scrape_with_social.py --all --days 7 --fb-posts 10 --tweets 10

# Scraper un média spécifique
python scrape_with_social.py --url https://www.aib.media --days 30

# Sans Facebook
python scrape_with_social.py --all --skip-facebook

# Sans Twitter
python scrape_with_social.py --all --skip-twitter
```

**Options :**

- `--all` : Scraper tous les médias actifs
- `--url URL` : Scraper un média spécifique
- `--days N` : Nombre de jours à récupérer (défaut: 7)
- `--fb-posts N` : Nombre de posts Facebook (défaut: 10)
- `--tweets N` : Nombre de tweets (défaut: 10)
- `--skip-facebook` : Ignorer Facebook
- `--skip-twitter` : Ignorer Twitter

#### 2. Classification thématique

```bash
# Classifier les articles non classifiés
python classify_articles.py

# Classifier les N derniers articles
python classify_articles.py --limit 100

# Reclassifier tous les articles
python classify_articles.py --reclassify
```

#### 3. Modération de contenu

```bash
# Modérer les contenus non analysés
python moderate_content.py

# Modérer les N derniers contenus
python moderate_content.py --limit 50

# Remodérer tous les contenus
python moderate_content.py --reanalyze
```

#### 4. Analyse d'audience

```bash
# Afficher l'analyse d'audience
python show_audience.py

# Période personnalisée
python show_audience.py --days 30
```

### Scraping automatique

Le scraping automatique est géré par le scheduler intégré. Configuration via l'API :

```bash
# Activer le scraping quotidien
curl -X PUT http://localhost:8000/api/scraping/schedule/ \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "frequency": "daily",
    "days": 7,
    "fb_posts": 10,
    "tweets": 10
  }'
```

## 🧩 Modules principaux

### 1. Scraper Manager ([scrapers/scraper_manager.py](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/backend/django_back/scrapers/scraper_manager.py:0:0-0:0))

Gestionnaire intelligent de scraping avec fallback automatique :

1. **RSS Feed** (prioritaire) - Rapide et fiable
2. **HTML Scraping** (fallback) - Si RSS indisponible

**Fonctionnalités :**

- Détection automatique du type de site
- Classification automatique après scraping
- Gestion des erreurs et retry
- Logging détaillé

### 2. Theme Classifier ([analysis/theme_classifier.py](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/backend/django_back/analysis/theme_classifier.py:0:0-0:0))

Classification thématique utilisant **Ollama + Mistral** :

**Catégories :**

- Politique
- Économie
- Sécurité
- Santé
- Culture
- Sport
- Autres

**Méthode :**

- Analyse du titre et contenu avec Mistral
- Score de confiance (0-1)
- Extraction de mots-clés
- Justification de la classification
- Fallback sur mots-clés si Ollama indisponible

### 3. Audience Analyzer ([analysis/audience_analyzer.py](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/backend/django_back/analysis/audience_analyzer.py:0:0-0:0))

Analyse d'audience multi-plateformes :

**Métriques Web :**

- Nombre d'articles
- Fréquence de publication
- Articles par jour
- Statut d'activité

**Métriques Facebook :**

- Posts, likes, commentaires, partages
- Engagement total et moyen
- Fréquence de publication

**Métriques Twitter :**

- Tweets, retweets, replies, likes
- Impressions
- Engagement total et moyen

**Score d'influence :**

- Composite : 40% volume + 60% engagement
- Classement des médias

### 4. Content Moderator (`analysis/content_moderator.py`)

Modération de contenu avec **Ollama + Mistral**:

**Détections :**

- **Toxicité** : discours haineux, violence, insultes, discrimination
- **Désinformation** : fake news, manipulation, propagande, théories du complot
- **Sensibilité** : contenu sensible nécessitant attention

**Scores :**

- Score de risque global (0-10)
- Niveau de risque : MINIMAL, FAIBLE, MOYEN, ÉLEVÉ, CRITIQUE
- Signalement automatique si nécessaire

### 5. Database Manager (`database/db_manager.py`)

Gestionnaire SQLite avec méthodes CRUD complètes :

**Fonctionnalités :**

- Gestion des médias, articles, classifications
- Posts Facebook et tweets
- Métriques d'audience
- Historique de scraping
- Modération de contenu
- Transactions sécurisées

## 🔐 Sécurité

### Configuration de production

**⚠️ Important pour la production :**

1. **Changer la SECRET_KEY** dans `settings.py`
2. **Désactiver DEBUG** : `DEBUG = False`
3. **Configurer ALLOWED_HOSTS** : liste des domaines autorisés
4. **Désactiver CORS_ALLOW_ALL_ORIGINS** : configurer les origines spécifiques
5. **Utiliser HTTPS** en production
6. **Configurer les permissions REST Framework** si nécessaire

### Variables sensibles

Utiliser des variables d'environnement pour :

- `SECRET_KEY`
- Clés API
- URLs de services externes
- Identifiants de base de données

## Optimisations

- **Index SQLite** sur colonnes fréquemment requêtées
- **Pagination** : 100 résultats par défaut
- **Cache** : possibilité d'ajouter Redis pour cache
- **Async** : possibilité de passer à Django Async pour scraping parallèle

### Limites actuelles

- SQLite : adapté jusqu'à ~100k articles
- Scraping synchrone : 1 média à la fois
- Ollama : nécessite ressources locales

### Évolutions possibles

- Migration vers PostgreSQL pour gros volumes
- Scraping asynchrone avec Celery
- Cache Redis
- API rate limiting
- Authentification JWT

## 🐛 Débogage

### Logs

Les logs sont affichés dans la console du serveur Django.

### Vérifier l'état de la base de données

```bash
python check_tables.py
```

### Tester les endpoints

```bash
# Health check
curl http://localhost:8000/api/health/

# Liste des médias
curl http://localhost:8000/api/medias/

# Articles récents
curl http://localhost:8000/api/articles/?days=7&limit=10
```

## 📝 License

Ce projet est développé dans le cadre du Media Scanner pour l'analyse des médias burkinabè.

## 👥 Contribution

Pour contribuer :

1. Fork le projet
2. Créer une branche feature
3. Commit les changements
4. Push vers la branche
5. Ouvrir une Pull Request

---

**Développé avec ❤️ pour l'analyse des médias burkinabè**
