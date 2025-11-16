# 📡 API REST - Media Scanner

## 🚀 Démarrage

### Installation des dépendances

```powershell
pip install -r requirements_api.txt
```

### Lancer le serveur

```powershell
python manage.py runserver
```

Le serveur démarre sur : **http://localhost:8000**

## 📚 Documentation interactive

- **Swagger UI** : http://localhost:8000/swagger/
- **ReDoc** : http://localhost:8000/redoc/
- **JSON Schema** : http://localhost:8000/swagger.json

## 🔗 Liste complète des endpoints

### 🏥 Health Check

#### GET /api/health/
Vérifier l'état de l'API

**Réponse** :
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

---

### 📺 Médias

#### GET /api/medias/
Liste tous les médias

**Réponse** :
```json
[
  {
    "id": 1,
    "nom": "AIB",
    "url": "https://www.aib.media",
    "type_site": "wordpress",
    "facebook_page": "aib.infos",
    "twitter_account": "aibburkina",
    "actif": true,
    "derniere_collecte": "2025-11-16T10:30:00Z",
    "created_at": "2025-11-01T00:00:00Z"
  }
]
```

#### GET /api/medias/{id}/
Détails d'un média spécifique

**Paramètres** :
- `id` : ID du média

---

### 📰 Articles

#### GET /api/articles/
Liste des articles

**Paramètres** :
- `media_id` (optionnel) : Filtrer par média
- `days` (défaut: 7) : Articles des X derniers jours
- `limit` (défaut: 100) : Nombre maximum d'articles

**Exemples** :
```
GET /api/articles/?media_id=1&limit=50
GET /api/articles/?days=30&limit=200
```

**Réponse** :
```json
[
  {
    "id": 1,
    "media_id": 1,
    "titre": "Titre de l'article",
    "contenu": "Contenu complet...",
    "extrait": "Résumé...",
    "url": "https://...",
    "auteur": "Nom Auteur",
    "date_publication": "2025-11-16T08:00:00Z",
    "image_url": "https://...",
    "categories": ["Politique"],
    "tags": ["tag1", "tag2"],
    "source_type": "wordpress_api",
    "vues": 0,
    "commentaires": 0,
    "scraped_at": "2025-11-16T10:00:00Z",
    "created_at": "2025-11-16T10:00:00Z"
  }
]
```

---

### 🏷️ Classifications

#### GET /api/classifications/
Liste des classifications thématiques

**Paramètres** :
- `categorie` (requis) : Catégorie à filtrer
- `limit` (défaut: 100) : Nombre maximum

**Catégories disponibles** :
- Politique
- Économie
- Sécurité
- Santé
- Culture
- Sport
- Autres

**Exemple** :
```
GET /api/classifications/?categorie=Politique&limit=50
```

#### GET /api/classifications/stats/
Statistiques par catégorie

**Paramètres** :
- `days` (défaut: 30) : Période d'analyse

**Réponse** :
```json
[
  {
    "categorie": "Politique",
    "total": 45,
    "confiance_moyenne": 0.85
  },
  {
    "categorie": "Économie",
    "total": 32,
    "confiance_moyenne": 0.78
  }
]
```

---

### 📘 Facebook

#### GET /api/facebook/posts/
Liste des posts Facebook

**Paramètres** :
- `media_id` (requis) : ID du média
- `limit` (défaut: 100) : Nombre maximum

**Exemple** :
```
GET /api/facebook/posts/?media_id=1&limit=50
```

**Réponse** :
```json
[
  {
    "id": 1,
    "media_id": 1,
    "post_id": "123456789_987654321",
    "message": "Contenu du post...",
    "url": "https://facebook.com/...",
    "image_url": "https://...",
    "date_publication": "2025-11-16T08:00:00Z",
    "likes": 150,
    "comments": 25,
    "shares": 10,
    "engagement_total": 185,
    "scraped_at": "2025-11-16T10:00:00Z"
  }
]
```

---

### 🐦 Twitter

#### GET /api/twitter/tweets/
Liste des tweets

**Paramètres** :
- `media_id` (requis) : ID du média
- `limit` (défaut: 100) : Nombre maximum

**Exemple** :
```
GET /api/twitter/tweets/?media_id=1&limit=50
```

**Réponse** :
```json
[
  {
    "id": 1,
    "media_id": 1,
    "tweet_id": "1234567890123456789",
    "text": "Contenu du tweet...",
    "url": "https://twitter.com/...",
    "image_url": "https://...",
    "date_publication": "2025-11-16T08:00:00Z",
    "retweets": 5,
    "replies": 3,
    "likes": 20,
    "quotes": 2,
    "impressions": 500,
    "engagement_total": 30,
    "scraped_at": "2025-11-16T10:00:00Z"
  }
]
```

---

### 📊 Audience

#### GET /api/audience/web/
Analyse de l'audience Web

**Paramètres** :
- `days` (défaut: 30) : Période d'analyse

**Réponse** :
```json
[
  {
    "id": 1,
    "nom": "AIB",
    "url": "https://www.aib.media",
    "total_articles": 20,
    "jours_avec_publication": 5,
    "articles_par_jour_moyen": 4.0,
    "derniere_publication": "2025-11-16T08:00:00Z",
    "jours_depuis_derniere_pub": 0,
    "statut": "🟢 Actif (aujourd'hui)"
  }
]
```

#### GET /api/audience/facebook/
Analyse de l'audience Facebook

**Paramètres** :
- `days` (défaut: 30) : Période d'analyse

**Réponse** :
```json
[
  {
    "id": 1,
    "nom": "AIB",
    "url": "https://www.aib.media",
    "facebook_page": "aib.infos",
    "total_posts": 5,
    "total_likes": 8920,
    "total_comments": 542,
    "total_shares": 1680,
    "engagement_total": 11142,
    "engagement_moyen": 2228.4,
    "jours_avec_publication": 3,
    "posts_par_jour_moyen": 1.67,
    "derniere_publication": "2025-11-16T08:00:00Z",
    "jours_depuis_derniere_pub": 0,
    "statut": "🟢 Actif (aujourd'hui)"
  }
]
```

#### GET /api/audience/twitter/
Analyse de l'audience Twitter

**Paramètres** :
- `days` (défaut: 30) : Période d'analyse

**Réponse** :
```json
[
  {
    "id": 1,
    "nom": "AIB",
    "url": "https://www.aib.media",
    "twitter_account": "aibburkina",
    "total_tweets": 5,
    "total_retweets": 10,
    "total_replies": 5,
    "total_likes": 50,
    "total_quotes": 2,
    "total_impressions": 1000,
    "engagement_total": 67,
    "engagement_moyen": 13.4,
    "jours_avec_publication": 2,
    "tweets_par_jour_moyen": 2.5,
    "derniere_publication": "2025-11-16T08:00:00Z",
    "jours_depuis_derniere_pub": 0,
    "statut": "🟢 Actif (aujourd'hui)"
  }
]
```

#### GET /api/audience/global/
Analyse globale (toutes plateformes)

**Paramètres** :
- `days` (défaut: 30) : Période d'analyse

**Réponse** :
```json
[
  {
    "id": 1,
    "nom": "AIB",
    "url": "https://www.aib.media",
    "total_publications": 30,
    "total_engagement": 11209,
    "score_influence": 68.25,
    "web": { /* données web */ },
    "facebook": { /* données facebook */ },
    "twitter": { /* données twitter */ }
  }
]
```

#### GET /api/audience/inactive/
Médias inactifs

**Paramètres** :
- `days_threshold` (défaut: 7) : Seuil d'inactivité en jours

**Réponse** :
```json
{
  "web": [
    {
      "nom": "Faso7",
      "jours_depuis_derniere_pub": 999
    }
  ],
  "facebook": [],
  "twitter": []
}
```

---

### 🏆 Classement

#### GET /api/ranking/
Classement des médias par influence

**Paramètres** :
- `days` (défaut: 30) : Période d'analyse

**Réponse** :
```json
[
  {
    "id": 1,
    "nom": "AIB",
    "url": "https://www.aib.media",
    "total_articles": 20,
    "total_posts_facebook": 5,
    "total_tweets": 5,
    "total_likes_fb": 8920,
    "total_comments_fb": 542,
    "total_shares_fb": 1680,
    "engagement_total_fb": 11142,
    "total_retweets": 10,
    "total_replies": 5,
    "total_likes_tw": 50,
    "total_quotes": 2,
    "total_impressions": 1000,
    "engagement_total_tw": 67,
    "engagement_total": 11209,
    "engagement_moyen": 1120.9
  }
]
```

---

### 🔄 Scraping

#### POST /api/scraping/trigger/
Déclencher un scraping

**Body** :
```json
{
  "url": "https://www.aib.media",
  "all": false,
  "days": 30,
  "fb_posts": 5,
  "tweets": 5,
  "skip_facebook": false,
  "skip_twitter": false
}
```

**Réponse** :
```json
{
  "status": "queued",
  "message": "Scraping en cours...",
  "total_articles": 0,
  "total_fb_posts": 0,
  "total_tweets": 0
}
```

---

### 📈 Statistiques

#### GET /api/stats/
Vue d'ensemble des statistiques

**Paramètres** :
- `days` (défaut: 30) : Période d'analyse

**Réponse** :
```json
{
  "total_medias": 10,
  "total_articles": 135,
  "total_categories": 7,
  "top_media": {
    "nom": "AIB",
    "engagement_total": 11209
  },
  "period_days": 30
}
```

---

## 🔧 Exemples d'utilisation

### Python (requests)

```python
import requests

# Liste des médias
response = requests.get('http://localhost:8000/api/medias/')
medias = response.json()

# Articles récents
response = requests.get('http://localhost:8000/api/articles/?days=7&limit=50')
articles = response.json()

# Audience Facebook
response = requests.get('http://localhost:8000/api/audience/facebook/?days=30')
audience = response.json()

# Classement
response = requests.get('http://localhost:8000/api/ranking/?days=30')
ranking = response.json()
```

### JavaScript (fetch)

```javascript
// Liste des médias
fetch('http://localhost:8000/api/medias/')
  .then(response => response.json())
  .then(data => console.log(data));

// Audience globale
fetch('http://localhost:8000/api/audience/global/?days=30')
  .then(response => response.json())
  .then(data => console.log(data));
```

### cURL

```bash
# Health check
curl http://localhost:8000/api/health/

# Liste des médias
curl http://localhost:8000/api/medias/

# Articles d'un média
curl "http://localhost:8000/api/articles/?media_id=1&limit=50"

# Classement
curl "http://localhost:8000/api/ranking/?days=30"
```

---

## 🚀 Prochaines étapes

1. **Installer les dépendances** : `pip install -r requirements_api.txt`
2. **Lancer le serveur** : `python manage.py runserver`
3. **Tester l'API** : http://localhost:8000/api/health/
4. **Explorer la doc** : http://localhost:8000/swagger/

**L'API REST est prête ! 🎉**
