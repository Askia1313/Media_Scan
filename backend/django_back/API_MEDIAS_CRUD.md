# API CRUD pour la gestion des Médias

## 📋 Vue d'ensemble

L'API permet maintenant de gérer complètement les médias depuis la table `medias` avec support pour :

- ✅ Scraping Web (URL)
- ✅ Scraping Facebook (facebook_page)
- ✅ Scraping Twitter (twitter_account)

## 🔗 Endpoints

### 1. Lister tous les médias

**GET** `/api/medias/`

**Query Parameters:**

- `actif` (optionnel): `true` pour ne récupérer que les médias actifs

**Exemple:**

```bash
GET /api/medias/
GET /api/medias/?actif=true
```

**Réponse:**

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
    "derniere_collecte": "2024-11-16T19:30:00Z",
    "created_at": "2024-11-01T10:00:00Z"
  }
]
```

---

### 2. Récupérer un média spécifique

**GET** `/api/medias/{id}/`

**Exemple:**

```bash
GET /api/medias/1/
```

**Réponse:**

```json
{
  "id": 1,
  "nom": "AIB",
  "url": "https://www.aib.media",
  "type_site": "wordpress",
  "facebook_page": "aib.infos",
  "twitter_account": "aibburkina",
  "actif": true,
  "derniere_collecte": "2024-11-16T19:30:00Z",
  "created_at": "2024-11-01T10:00:00Z"
}
```

---

### 3. Créer un nouveau média

**POST** `/api/medias/`

**Body (JSON):**

```json
{
  "nom": "Lefaso",
  "url": "https://lefaso.net",
  "type_site": "wordpress",
  "facebook_page": "lefasonet",
  "twitter_account": "lefasonet",
  "actif": true
}
```

**Champs obligatoires:**

- `nom`: Nom du média
- `url`: URL du site web

**Champs optionnels:**

- `type_site`: Type de site (wordpress, html, rss, unknown)
- `facebook_page`: Nom/ID de la page Facebook
- `twitter_account`: Nom du compte Twitter (sans @)
- `actif`: Statut actif/inactif (défaut: true)

**Réponse (201 Created):**

```json
{
  "id": 2,
  "nom": "Lefaso",
  "url": "https://lefaso.net",
  "type_site": "wordpress",
  "facebook_page": "lefasonet",
  "twitter_account": "lefasonet",
  "actif": true,
  "derniere_collecte": null,
  "created_at": "2024-11-16T20:00:00Z"
}
```

---

### 4. Mettre à jour un média

**PUT** `/api/medias/{id}/`

**Body (JSON) - Tous les champs sont optionnels:**

```json
{
  "nom": "AIB Média",
  "facebook_page": "aib.media.officiel",
  "actif": true
}
```

**Exemple:**

```bash
PUT /api/medias/1/
Content-Type: application/json

{
  "facebook_page": "aib.media.officiel",
  "twitter_account": "aibmedia"
}
```

**Réponse (200 OK):**

```json
{
  "id": 1,
  "nom": "AIB",
  "url": "https://www.aib.media",
  "type_site": "wordpress",
  "facebook_page": "aib.media.officiel",
  "twitter_account": "aibmedia",
  "actif": true,
  "derniere_collecte": "2024-11-16T19:30:00Z",
  "created_at": "2024-11-01T10:00:00Z"
}
```

---

### 5. Supprimer un média

**DELETE** `/api/medias/{id}/`

**Exemple:**

```bash
DELETE /api/medias/5/
```

**Réponse (204 No Content):**

```json
{
  "message": "Média supprimé avec succès"
}
```

**⚠️ Attention:** La suppression d'un média supprime également :

- Tous ses articles
- Tous ses posts Facebook
- Tous ses tweets
- Toutes ses métriques

---

## 🚀 Utilisation avec les scrapers

### Scraping Web

Les scrapers web lisent automatiquement depuis la table `medias` :

```bash
# Scraper tous les médias actifs
python run_scraper.py

# Scraper un média spécifique
python run_scraper.py --url https://www.aib.media
```

### Scraping Facebook

```bash
# Scraper tous les médias avec Facebook configuré
python scrape_facebook.py --all

# Scraper un média spécifique
python scrape_facebook.py --media-id 1 --limit 20
```

### Scraping Twitter

```bash
# Scraper tous les médias avec Twitter configuré
python scrape_twitter.py --all

# Scraper un média spécifique
python scrape_twitter.py --media-id 1 --limit 20
```

### Scraping complet (Web + Facebook + Twitter)

```bash
# Scraper tous les médias sur toutes les plateformes
python scrape_with_social.py --all

# Scraper un média spécifique
python scrape_with_social.py --url https://www.aib.media

# Scraper sans Facebook
python scrape_with_social.py --all --skip-facebook

# Scraper sans Twitter
python scrape_with_social.py --all --skip-twitter
```

---

## 📊 Exemples d'utilisation

### Ajouter un nouveau média avec toutes les plateformes

```bash
curl -X POST http://localhost:8000/api/medias/ \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Burkina24",
    "url": "https://burkina24.com",
    "type_site": "wordpress",
    "facebook_page": "burkina24",
    "twitter_account": "burkina24bf"
  }'
```

### Désactiver temporairement un média

```bash
curl -X PUT http://localhost:8000/api/medias/3/ \
  -H "Content-Type: application/json" \
  -d '{"actif": false}'
```

### Mettre à jour uniquement le compte Twitter

```bash
curl -X PUT http://localhost:8000/api/medias/1/ \
  -H "Content-Type: application/json" \
  -d '{"twitter_account": "nouveau_compte"}'
```

---

## 🔍 Filtres et recherches

### Récupérer uniquement les médias actifs

```bash
GET /api/medias/?actif=true
```

### Récupérer les médias avec Facebook

Utilisez la méthode du `db_manager`:

```python
from database.db_manager import DatabaseManager
db = DatabaseManager()
medias = db.get_medias_with_facebook(actif_only=True)
```

### Récupérer les médias avec Twitter

```python
medias = db.get_medias_with_twitter(actif_only=True)
```

### Récupérer les médias pour scraping web

```python
medias = db.get_medias_for_web_scraping(actif_only=True)
```

---

## ✅ Validation des données

### Champ `url`

- Doit être une URL valide
- Doit être unique dans la base

### Champ `nom`

- Obligatoire
- Maximum 200 caractères

### Champ `facebook_page`

- Optionnel
- Nom de la page Facebook (sans facebook.com/)
- Exemple: `aib.infos` pour `facebook.com/aib.infos`

### Champ `twitter_account`

- Optionnel
- Nom du compte Twitter (sans @)
- Exemple: `aibburkina` pour `@aibburkina`

---

## 🔐 Sécurité

- Les tokens Facebook et Twitter doivent être configurés dans `.env`
- Les endpoints API sont accessibles sans authentification (à sécuriser en production)
- La suppression de médias est définitive et cascade sur toutes les données liées

---

## 📝 Notes importantes

1. **Migration depuis fichiers texte**: Les données des fichiers `sites.txt`, `facebook_pages.txt` et `twitter_accounts.txt` doivent être importées dans la table `medias`

2. **Compatibilité**: Les anciens scripts continuent de fonctionner mais utilisent maintenant la table `medias`

3. **Scraping automatique**: Les scrapers lisent automatiquement les médias actifs depuis la base de données

4. **Gestion centralisée**: Toute la configuration des médias est maintenant dans la base de données, modifiable via l'API

---

## 🐛 Gestion des erreurs

### 400 Bad Request

```json
{
  "nom": ["Ce champ est obligatoire"],
  "url": ["Entrez une URL valide"]
}
```

### 404 Not Found

```json
{
  "error": "Média non trouvé"
}
```

### 500 Internal Server Error

```json
{
  "error": "Message d'erreur détaillé"
}
```
