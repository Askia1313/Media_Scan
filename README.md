# ÉDIA-SCAN - Système Intelligent d'Observation des Médias

> Plateforme d'intelligence artificielle pour la surveillance et l'analyse automatique des médias burkinabè

* **Hackathon MTDPCE AI 2025 - Challenge Gouvernance & Transparence Médiatique**

---

## 📋 Table des Matières

* [Vue d&#39;Ensemble](#-vue-densemble)
* [Architecture](#-architecture)
* [Stack Technique](#-stack-technique)
* [Plan 72h](#-plan-de-développement-72h)
* [Installation](#-installation)
* [Développement Détaillé](#-développement-détaillé)
* [Utilisation](#-utilisation)
* [Déploiement](#-déploiement)

---

## 🎯 Vue d'Ensemble

### Objectif

Développer une plateforme IA capable de :

✅ **Collecter** automatiquement 100+ contenus de 5 médias burkinabè
✅ **Classifier** par thématique avec ML (7 catégories)
✅ **Mesurer** l'audience et calculer scores d'influence
✅ **Détecter** contenus sensibles (haine, désinformation)
✅ **Dashboard** interactif avec exports PDF/Excel

### Sources de Données

**Sites Web** : Lefaso.net, Sidwaya, FasoPresse, Observateur Paalga, AIB
**Facebook** : 5 pages médias (avec compte personnel)
**Twitter** : Via Nitter (proxy gratuit)
**YouTube** : API gratuite + transcriptions

### Critères de Succès

| Critère    | Minimum | Excellence             |
| ----------- | ------- | ---------------------- |
| Articles    | 100+    | 1000+                  |
| Médias     | 5       | 10+                    |
| ML Accuracy | >60%    | >80%                   |
| Sources     | Web     | Web + Réseaux sociaux |

---

## 🏗️ Architecture

```
media-scan/
├── scrapers/          # Collecte (web, Facebook, Twitter, YouTube)
├── classifier/        # Classification ML
├── analytics/         # Scores d'influence
├── detection/         # Contenus sensibles
├── database/          # SQLite + schema
├── dashboard/         # Streamlit
├── data/             # Données collectées
├── models/           # Modèles ML
└── requirements.txt
```

---

## 🛠️ Stack Technique

**Scraping** : BeautifulSoup, Selenium, youtube-transcript-api
**ML/NLP** : scikit-learn, spaCy, NLTK
**Dashboard** : Streamlit, Plotly
**Database** : SQLite
**Export** : reportlab (PDF), openpyxl (Excel)

**💰 Coût : 0€** (100% gratuit, pas d'API payante)

---

## 📅 Plan de Développement (72h)

### JOUR 1 (24h) - Setup & Collecte

**0-2h** : Setup environnement + dépendances
**2-3h** : Base de données SQLite
**3-8h** : Scraper sites web (BeautifulSoup)
**8-14h** : Scraper Facebook (Selenium)
**14-16h** : Script principal collecte
**16-24h** : Tests & enrichissement

**Livrable** : 250+ articles collectés ✅

### JOUR 2 (24h) - Intelligence Artificielle

**24-32h** : Classification ML (scikit-learn)
**32-36h** : Calcul scores d'influence
**36-40h** : Détection contenus sensibles
**40-48h** : Tests & optimisation

**Livrable** : Modèles ML fonctionnels ✅

### JOUR 3 (24h) - Dashboard & Finitions

**48-60h** : Dashboard Streamlit complet
**60-64h** : Export rapports (PDF/Excel)
**64-68h** : Documentation
**68-72h** : Démo + présentation

**Livrable** : Projet complet déployable ✅

---

## 💻 Installation

### Prérequis

- Python 3.9+
- Chrome/Firefox (pour Selenium)
- 4GB RAM minimum

### Setup Rapide

```bash
# 1. Cloner/Créer le projet
mkdir media-scan && cd media-scan

# 2. Environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Télécharger modèles NLP
python -m spacy download fr_core_news_sm
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# 5. Initialiser la base de données
python -c "from database.db_manager import DatabaseManager; DatabaseManager()"
```

### requirements.txt

```txt
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2
youtube-transcript-api==0.6.1
pandas==2.1.3
scikit-learn==1.3.2
nltk==3.8.1
spacy==3.7.2
streamlit==1.28.2
plotly==5.18.0
reportlab==4.0.7
openpyxl==3.1.2
tqdm==4.66.1
python-dotenv==1.0.0
```

---

## 📖 Développement Détaillé

### JOUR 1 - Collecte de Données

#### 1. Base de Données (database/schema.sql)

```sql
CREATE TABLE medias (
    id INTEGER PRIMARY KEY,
    nom TEXT UNIQUE,
    type TEXT,
    url TEXT
);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    media_id INTEGER,
    titre TEXT,
    contenu TEXT,
    url TEXT UNIQUE,
    date_publication TIMESTAMP,
    source_type TEXT,
    categorie TEXT,
    likes INTEGER DEFAULT 0,
    partages INTEGER DEFAULT 0,
    commentaires INTEGER DEFAULT 0,
    sensible BOOLEAN DEFAULT 0,
    toxicite_score REAL DEFAULT 0,
    FOREIGN KEY (media_id) REFERENCES medias(id)
);

CREATE INDEX idx_articles_media ON articles(media_id);
CREATE INDEX idx_articles_date ON articles(date_publication);
```

#### 2. Scraper Web (scrapers/web_scraper.py)

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        })
  
    def scrape_lefaso(self):
        """Scraper Lefaso.net"""
        print("📰 Scraping Lefaso.net...")
        articles = []
  
        try:
            response = self.session.get('https://lefaso.net', timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
      
            # Adapter selon structure réelle
            article_elements = soup.find_all('article')[:50]
      
            for elem in article_elements:
                titre = elem.find('h2') or elem.find('h3')
                lien = elem.find('a')
          
                if titre and lien:
                    url = lien.get('href')
                    if not url.startswith('http'):
                        url = 'https://lefaso.net' + url
              
                    contenu = self.get_content(url)
              
                    articles.append({
                        'titre': titre.text.strip(),
                        'contenu': contenu,
                        'url': url,
                        'date_publication': datetime.now().isoformat(),
                        'source': 'Lefaso.net'
                    })
          
                time.sleep(1)
  
        except Exception as e:
            print(f"❌ Erreur: {e}")
  
        print(f"✅ {len(articles)} articles collectés")
        return articles
  
    def get_content(self, url):
        """Extraire contenu article"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            return ' '.join([p.text.strip() for p in paragraphs[:10]])[:2000]
        except:
            return ""
```

#### 3. Scraper Facebook (scrapers/facebook_scraper.py)

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

class FacebookScraper:
    def __init__(self):
        options = Options()
        options.add_argument('--user-data-dir=./fb_profile')
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=options)
  
    def login_manual(self):
        """Connexion manuelle (une fois)"""
        self.driver.get('https://www.facebook.com')
        input("⏸️  Connectez-vous, puis Entrée...")
        print("✅ Session sauvegardée")
  
    def scrape_page(self, page_url, media_name):
        """Scraper une page Facebook"""
        print(f"📱 Scraping {media_name}...")
        self.driver.get(page_url)
        time.sleep(5)
  
        posts = []
        for i in range(10):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
      
            elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-ad-preview="message"]')
      
            for elem in elements:
                try:
                    text = elem.text
                    engagement = self.extract_engagement(text)
              
                    post = {
                        'titre': text[:100],
                        'contenu': text[:2000],
                        'url': page_url,
                        'date_publication': datetime.now().isoformat(),
                        'source': media_name,
                        **engagement
                    }
              
                    if post not in posts:
                        posts.append(post)
                except:
                    continue
  
        print(f"✅ {len(posts)} posts collectés")
        return posts
  
    def extract_engagement(self, text):
        """Extraire likes, partages, commentaires"""
        engagement = {'likes': 0, 'partages': 0, 'commentaires': 0}
        text_lower = text.lower()
  
        likes_match = re.search(r'(\d+)\s*(j\'aime|like)', text_lower)
        if likes_match:
            engagement['likes'] = int(likes_match.group(1))
  
        shares_match = re.search(r'(\d+)\s*(partage|share)', text_lower)
        if shares_match:
            engagement['partages'] = int(shares_match.group(1))
  
        comments_match = re.search(r'(\d+)\s*(commentaire|comment)', text_lower)
        if comments_match:
            engagement['commentaires'] = int(comments_match.group(1))
  
        return engagement
```

#### 4. Script Principal (collect_data.py)

```python
from database.db_manager import DatabaseManager
from scrapers.web_scraper import WebScraper
from scrapers.facebook_scraper import FacebookScraper

FACEBOOK_PAGES = {
    'Lefaso.net': 'https://www.facebook.com/lefasonet',
    'Sidwaya': 'https://www.facebook.com/sidwayanews',
    'FasoPresse': 'https://www.facebook.com/fasopresse',
    'Observateur Paalga': 'https://www.facebook.com/observateurpaalga',
    'AIB': 'https://www.facebook.com/aibburkina'
}

def main():
    print("🚀 MÉDIA-SCAN - Collecte")
    print("="*60)
  
    db = DatabaseManager()
  
    # 1. Sites Web
    print("\n📰 PHASE 1: Sites Web")
    web_scraper = WebScraper()
    web_articles = web_scraper.scrape_lefaso()
  
    for article in web_articles:
        media_id = db.add_media(article['source'], 'web', article.get('url', ''))
        article['media_id'] = media_id
        article['source_type'] = 'web'
        db.add_article(article)
  
    print(f"✅ {len(web_articles)} articles web sauvegardés")
  
    # 2. Facebook
    print("\n📱 PHASE 2: Facebook")
    fb_scraper = FacebookScraper()
    fb_scraper.login_manual()
    fb_posts = fb_scraper.scrape_all(FACEBOOK_PAGES)
  
    for post in fb_posts:
        media_id = db.add_media(post['source'], 'facebook', post.get('url', ''))
        post['media_id'] = media_id
        post['source_type'] = 'facebook'
        db.add_article(post)
  
    print(f"✅ {len(fb_posts)} posts Facebook sauvegardés")
  
    total = len(web_articles) + len(fb_posts)
    print(f"\n🎉 TOTAL: {total} contenus collectés")

if __name__ == '__main__':
    main()
```

### JOUR 2 - Intelligence Artificielle

#### 5. Classification ML (classifier/ml_classifier.py)

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle

CATEGORIES = ['Politique', 'Économie', 'Sécurité', 'Santé', 'Culture', 'Sport', 'Autres']

class MLClassifier:
    def __init__(self):
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
            ('clf', MultinomialNB())
        ])
  
    def train_with_keywords(self):
        """Entraîner avec mots-clés"""
        training_data = [
            ("élection président gouvernement ministre politique", "Politique"),
            ("économie croissance PIB entreprise commerce", "Économie"),
            ("terrorisme sécurité armée police attaque", "Sécurité"),
            ("santé hôpital maladie médecin vaccination", "Santé"),
            ("culture festival musique cinéma art", "Culture"),
            ("football sport match championnat équipe", "Sport"),
        ] * 20
  
        texts = [t[0] for t in training_data]
        labels = [t[1] for t in training_data]
  
        self.model.fit(texts, labels)
        print("✅ Modèle entraîné")
  
    def predict(self, text):
        return self.model.predict([text])[0]
  
    def save(self, path='models/classifier.pkl'):
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
```

#### 6. Scores d'Influence (analytics/influence_score.py)

```python
import sqlite3
import pandas as pd

class InfluenceAnalyzer:
    def __init__(self, db_path='data/media_scan.db'):
        self.db_path = db_path
  
    def calculate_scores(self):
        conn = sqlite3.connect(self.db_path)
  
        query = """
        SELECT 
            m.nom as media,
            COUNT(a.id) as nb_publications,
            SUM(a.likes + a.partages + a.commentaires) as engagement_total
        FROM medias m
        LEFT JOIN articles a ON m.id = a.media_id
        GROUP BY m.id
        """
  
        df = pd.read_sql_query(query, conn)
  
        # Score d'influence (0-10)
        max_pub = df['nb_publications'].max()
        max_eng = df['engagement_total'].max()
  
        df['score_influence'] = (
            (df['nb_publications'] / max_pub * 0.3) +
            (df['engagement_total'] / max_eng * 0.7)
        ) * 10
  
        df['rang'] = df['score_influence'].rank(ascending=False).astype(int)
  
        print("\n📊 Classement des Médias:")
        print(df[['rang', 'media', 'score_influence']])
  
        return df
```

#### 7. Détection Toxicité (detection/toxicity_detector.py)

```python
class ToxicityDetector:
    def __init__(self):
        self.hate_keywords = [
            'haine', 'tuer', 'mort', 'violence', 'terroriste',
            'guerre', 'attaque', 'conflit', 'massacre'
        ]
  
    def detect_toxicity(self, text):
        if not text:
            return False, 0.0
  
        text_lower = text.lower()
        score = sum(1 for kw in self.hate_keywords if kw in text_lower)
  
        toxicity_score = min(score / len(self.hate_keywords), 1.0)
        is_toxic = toxicity_score > 0.3
  
        return is_toxic, toxicity_score
```

### JOUR 3 - Dashboard

#### 8. Dashboard Streamlit (dashboard/app.py)

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(page_title="MÉDIA-SCAN", page_icon="📰", layout="wide")

conn = sqlite3.connect('data/media_scan.db')

st.title("📰 MÉDIA-SCAN - Observatoire des Médias Burkinabè")

# Métriques
col1, col2, col3, col4 = st.columns(4)

total_articles = pd.read_sql("SELECT COUNT(*) as c FROM articles", conn).iloc[0]['c']
total_medias = pd.read_sql("SELECT COUNT(*) as c FROM medias", conn).iloc[0]['c']
engagement = pd.read_sql("SELECT SUM(likes+partages+commentaires) as e FROM articles", conn).iloc[0]['e'] or 0
toxic = pd.read_sql("SELECT COUNT(*) as c FROM articles WHERE sensible=1", conn).iloc[0]['c']

col1.metric("📄 Articles", f"{total_articles:,}")
col2.metric("📺 Médias", total_medias)
col3.metric("💬 Engagement", f"{int(engagement):,}")
col4.metric("⚠️ Sensibles", toxic)

# Graphiques
tab1, tab2 = st.tabs(["📊 Distribution", "🏆 Classement"])

with tab1:
    df_cat = pd.read_sql("""
        SELECT categorie, COUNT(*) as count
        FROM articles WHERE categorie IS NOT NULL
        GROUP BY categorie
    """, conn)
  
    fig = px.bar(df_cat, x='categorie', y='count', title="Articles par Thématique")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    df_rank = pd.read_sql("""
        SELECT m.nom, COUNT(a.id) as pubs,
               SUM(a.likes+a.partages+a.commentaires) as eng
        FROM medias m
        LEFT JOIN articles a ON m.id = a.media_id
        GROUP BY m.id ORDER BY eng DESC
    """, conn)
  
    st.dataframe(df_rank, use_container_width=True)
```

---

## 🎮 Utilisation

### Collecter les Données

```bash
python collect_data.py
```

### Classifier les Articles

```bash
python -c "from classifier.ml_classifier import MLClassifier; clf = MLClassifier(); clf.train_with_keywords(); clf.save()"
```

### Lancer le Dashboard

```bash
streamlit run dashboard/app.py
```

Ouvrir : http://localhost:8501

---

## 🚀 Déploiement

### Local

```bash
streamlit run dashboard/app.py --server.port 8501
```

### Streamlit Cloud (Gratuit)

1. Push sur GitHub
2. Connecter à streamlit.io
3. Déployer automatiquement

---

## 📊 Résultats Attendus

- **250+ articles** collectés (Jour 1)
- **Classification ML** >80% accuracy (Jour 2)
- **Dashboard interactif** complet (Jour 3)
- **Rapports exportables** PDF/Excel
- **Détection contenus sensibles** fonctionnelle

---

## 🤝 Contribution

Développé pour le **Hackathon MTDPCE AI 2025**
Challenge : Gouvernance & Transparence Médiatique

---

## 📄 Licence

MIT License - Projet Open Source

---

## 📞 Support

Pour questions : [Votre contact]

**🎉 Bon développement !**
