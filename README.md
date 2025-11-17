📰 CSC Média Monitor

**Plateforme complète de surveillance, d'analyse et de modération des médias burkinabè**

Système full-stack permettant le scraping automatique d'articles de presse, de posts Facebook et de tweets, avec classification thématique par IA, analyse d'audience multi-plateformes et modération de contenu.

[![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8.3-blue.svg)](https://www.typescriptlang.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4.17-38B2AC.svg)](https://tailwindcss.com/)

## 🎯 Vue d'ensemble

CSC Média Monitor est une solution complète pour :

- 🔍 **Scraper automatiquement** les sites web, pages Facebook et comptes Twitter des médias
- 🏷️ **Classifier automatiquement** les articles par thématique (Politique, Économie, Sécurité, etc.)
- 📊 **Analyser l'audience** et l'engagement sur toutes les plateformes
- 🛡️ **Modérer le contenu** (détection de toxicité, désinformation, contenu sensible)
- 📈 **Visualiser les données** via un dashboard interactif
- 📄 **Générer des rapports** PDF et Excel

## 🏗️ Architecture

```
Media_Scanne/
├── backend/                    # API REST Django
│   └── django_back/
│       ├── api/               # Endpoints REST
│       ├── database/          # Gestion SQLite
│       ├── scrapers/          # Modules de scraping
│       ├── analysis/          # IA & Analyse
│       └── utils/             # Utilitaires
│
├── frontend/                   # Interface React/TypeScript
│   └── src/
│       ├── components/        # Composants UI
│       ├── services/          # Services API
│       ├── hooks/             # Custom hooks
│       └── pages/             # Pages
│
└── data/
    └── media_scan.db          # Base de données SQLite
```

## ✨ Fonctionnalités principales

### 🔄 Scraping Multi-Sources

- **Sites Web** : RSS Feed + HTML scraping intelligent
- **Facebook** : Posts, likes, commentaires, partages
- **Twitter** : Tweets, retweets, replies, impressions
- **Automatisation** : Scraping planifié (horaire, quotidien, hebdomadaire)
- **Fallback** : Basculement automatique RSS → HTML si échec

### 🤖 Intelligence Artificielle

**Classification Thématique (Ollama + Mistral)**

- 7 catégories : Politique, Économie, Sécurité, Santé, Culture, Sport, Autres
- Score de confiance
- Extraction de mots-clés
- Justification de la classification

**Modération de Contenu (Ollama + Mistral)**

- Détection de toxicité (discours haineux, violence, insultes)
- Détection de désinformation (fake news, manipulation, propagande)
- Analyse de sensibilité
- Niveaux de risque : MINIMAL, FAIBLE, MOYEN, ÉLEVÉ, CRITIQUE

### 📊 Analyse d'Audience

**Métriques Web**

- Nombre d'articles
- Fréquence de publication
- Statut d'activité

**Métriques Facebook**

- Engagement total (likes + commentaires + partages)
- Engagement moyen par post
- Fréquence de publication

**Métriques Twitter**

- Engagement total (retweets + replies + likes + quotes)
- Impressions
- Engagement moyen par tweet

**Score d'Influence**

- Composite : 40% volume + 60% engagement
- Classement des médias

### 📈 Dashboard Interactif

- **Vue d'ensemble** : KPIs, graphiques, derniers articles
- **Classement** : Médias par engagement
- **Analyse thématique** : Distribution et évolution
- **Alertes** : Contenus sensibles signalés
- **Contrôle** : Déclenchement et planification du scraping
- **Gestion** : CRUD des médias

### 📄 Génération de Rapports

- **Format PDF** : Rapports professionnels avec graphiques
- **Format Excel** : Données brutes exportables
- **Période personnalisable**

## 🛠️ Stack Technique

### Backend

- **Django 5.2.8** - Framework web Python
- **Django REST Framework 3.14.0** - API REST
- **SQLite 3** - Base de données
- **BeautifulSoup4** - Parsing HTML
- **Feedparser** - Parsing RSS
- **Ollama + Mistral** - Classification IA
- **Ollama + Mistral** - Modération IA

### Frontend

- **React 18.3.1** - Bibliothèque UI
- **TypeScript 5.8.3** - Typage statique
- **Vite 5.4.19** - Build tool
- **TanStack Query 5.83.0** - State management
- **TailwindCSS 3.4.17** - Framework CSS
- **shadcn/ui** - Composants UI (40+)
- **Recharts 2.15.4** - Graphiques
- **jsPDF + xlsx** - Génération de rapports

## 🚀 Installation Rapide

### Prérequis

- Python 3.10+
- Node.js 18+
- Ollama (optionnel, pour IA)

### 1. Cloner le projet

```bash
git clone <repository-url>
cd Media_Scanne
```

### 2. Backend

```bash
cd backend/django_back

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python manage.py runserver
```

Le backend démarre sur `http://localhost:8000`

**Documentation API :** `http://localhost:8000/swagger/`

### 3. Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Configurer l'API
echo "VITE_API_URL=http://localhost:8000" > .env

# Lancer le serveur
npm run dev
```

Le frontend démarre sur `http://localhost:8080`

### 4. Ollama

Pour activer la classification et la modération par IA :

```bash
# Installer Ollama
# https://ollama.ai/

# Télécharger les modèles
ollama pull mistral

# Lancer Ollama
ollama serve
```

## 📖 Documentation Détaillée

- **[Backend README](./backend/README.md)** - Documentation complète du backend
- **[Frontend README](./frontend/README.md)** - Documentation complète du frontend

## 🎮 Utilisation

### Démarrage rapide

1. **Ajouter un média** (onglet "Médias")

   - Nom : AIB
   - URL : https://www.aib.media
   - Type : wordpress
   - Compte Twitter : AibBurkina
2. **Lancer un scraping** (onglet "Scraping")

   - Sélectionner "Tous les médias"
   - Configurer les paramètres
   - Cliquer sur "Démarrer le scraping"
3. **Visualiser les résultats**

   - Onglet "Vue d'ensemble" : statistiques globales
   - Onglet "Classement" : médias par engagement
   - Onglet "Thématiques" : distribution des articles
4. **Configurer l'automatisation** (onglet "Contrôle")

   - Activer le scraping automatique
   - Choisir la fréquence
   - Enregistrer

### Scripts CLI

#### Scraping complet

```bash
cd backend/django_back

# Scraper tous les médias
python scrape_with_social.py --all --days 7

# Scraper un média spécifique
python scrape_with_social.py --url https://www.aib.media --days 30
```

#### Classification

```bash
# Classifier les articles non classifiés
python classify_articles.py

# Reclassifier tous les articles
python classify_articles.py --reclassify
```

#### Modération

```bash
# Modérer les contenus non analysés
python moderate_content.py

# Remodérer tous les contenus
python moderate_content.py --reanalyze
```

#### Analyse d'audience

```bash
# Afficher l'analyse d'audience
python show_audience.py --days 30
```

## 📊 API REST

### Endpoints principaux

```
GET    /api/health/                    # Health check
GET    /api/medias/                    # Liste des médias
POST   /api/medias/                    # Créer un média
GET    /api/articles/                  # Liste des articles
GET    /api/classifications/stats/     # Stats par catégorie
GET    /api/twitter/tweets/            # Tweets
GET    /api/audience/global/           # Audience globale
GET    /api/ranking/                   # Classement des médias
POST   /api/scraping/trigger/          # Déclencher scraping
GET    /api/scraping/schedule/         # Config automatique
GET    /api/moderation/flagged/        # Contenus signalés
GET    /api/stats/                     # Statistiques globales
```

**Documentation complète :** `http://localhost:8000/swagger/`

## 🗄️ Base de Données

### Tables principales

- **medias** : Médias surveillés
- **articles** : Articles collectés
- **classifications** : Classifications thématiques
- **facebook_posts** : Posts Facebook
- **twitter_tweets** : Tweets
- **content_moderation** : Analyses de modération
- **scraping_tasks** : Historique des tâches
- **scraping_schedule** : Configuration automatique

**Schéma complet :** [backend/django_back/database/schema.sql](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/backend/django_back/database/schema.sql:0:0-0:0)

## 🔐 Configuration

### Backend (.env)

```env
FACEBOOK_ACCESS_TOKEN=......
TWITTER_BEARER_TOKEN=........
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## 🎨 Captures d'écran

### Dashboard

![Dashboard Overview](docs/screenshots/dashboard.png)

### Scraping Control

![Scraping Control](docs/screenshots/scraping.png)

### Media Ranking

![Media Ranking](docs/screenshots/ranking.png)

### Thematic Analysis

![Thematic Analysis](docs/screenshots/themes.png)

## 🔒 Sécurité

### Production

**⚠️ Important avant déploiement :**

1. Changer `SECRET_KEY` Django
2. Désactiver `DEBUG = False`
3. Configurer `ALLOWED_HOSTS`
4. Désactiver `CORS_ALLOW_ALL_ORIGINS`
5. Utiliser HTTPS
6. Configurer un reverse proxy (Nginx)
7. Utiliser des variables d'environnement

### Recommandations

- Ne jamais commiter les fichiers [.env](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/backend/django_back/.env:0:0-0:0)
- Utiliser des secrets management tools
- Activer l'authentification si nécessaire
- Limiter les taux d'API (rate limiting)
- Sauvegarder régulièrement la base de données

## 🐛 Débogage

### Backend

```bash
# Vérifier l'état de la base de données
python check_tables.py

# Tester les endpoints
curl http://localhost:8000/api/health/

# Logs Django
python manage.py runserver --verbosity 2
```

### Frontend

```bash
# Mode développement avec logs
npm run dev

# Build de test
npm run build:dev

# Analyser le bundle
npm run build -- --mode analyze
```

### Problèmes courants

**Ollama non accessible**

- Vérifier : `curl http://localhost:11434/api/tags`
- Solution : `ollama serve`

**CORS errors**

- Vérifier `CORS_ALLOWED_ORIGINS` dans Django settings
- En dev : `CORS_ALLOW_ALL_ORIGINS = True`

**Base de données verrouillée**

- Fermer toutes les connexions
- Redémarrer le serveur Django

## 📦 Déploiement

### Backend (Django)

```bash
# Build
python manage.py collectstatic

# Serveur WSGI (Gunicorn)
gunicorn django_back.wsgi:application --bind 0.0.0.0:8000
```

### Frontend (React)

```bash
# Build de production
npm run build

# Les fichiers sont dans dist/
# Servir avec Nginx, Apache, Vercel, Netlify, etc.
```

### Docker (à venir)

```bash
docker-compose up -d
```

## 🤝 Contribution

### Workflow

1. Fork le projet
2. Créer une branche : `git checkout -b feature/nouvelle-fonctionnalite`
3. Commit : `git commit -m "Ajout de nouvelle fonctionnalité"`
4. Push : `git push origin feature/nouvelle-fonctionnalite`
5. Ouvrir une Pull Request

### Standards

- **Python** : PEP 8
- **TypeScript** : ESLint + Prettier
- **Commits** : Messages descriptifs
- **Tests** : Ajouter des tests pour les nouvelles fonctionnalités

## 📝 Changelog

### Version 1.0.0 (Actuelle)

- ✅ Scraping multi-sources (Web, Facebook, Twitter)
- ✅ Classification thématique par IA
- ✅ Modération de contenu
- ✅ Analyse d'audience multi-plateformes
- ✅ Dashboard interactif
- ✅ Génération de rapports PDF/Excel
- ✅ Scraping automatique planifié
- ✅ API REST complète
- ✅ Documentation Swagger

## 🗺️ Roadmap

### Version 1.1

- [ ] Authentification utilisateurs
- [ ] Rôles et permissions
- [ ] Notifications en temps réel
- [ ] Export de rapports personnalisés

### Version 1.2

- [ ] Support PostgreSQL
- [ ] Scraping asynchrone (Celery)
- [ ] Cache Redis
- [ ] API rate limiting

### Version 1.3

- [ ] Analyse de sentiment
- [ ] Détection d'entités (NER)
- [ ] Clustering d'articles similaires
- [ ] Recommandations

### Version 2.0

- [ ] Multi-tenancy
- [ ] API GraphQL
- [ ] Mobile app (React Native)
- [ ] Webhooks

## 📄 License

Ce projet est développé dans le cadre du CSC Média Monitor pour l'analyse des médias burkinabè.

## 👥 Équipe

- BILA Djamel Franck Chérubin
- KONATE Askia Rachid Mounir Fahran

## 📞 Support

- **Documentation** : Voir README backend et frontend
- **Email** : bilafranck09@gmail.com  et  konateaskia1@gmail.com

---

**Développé avec ❤️ pour l'analyse des médias burkinabè**

**CSC Média Monitor** - Plateforme de surveillance et d'analyse des médias
