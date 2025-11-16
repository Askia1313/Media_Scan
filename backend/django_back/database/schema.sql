-- Schéma de base de données SQLite pour MÉDIA-SCAN

-- Table des médias
CREATE TABLE IF NOT EXISTS medias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    type_site TEXT DEFAULT 'unknown',  -- wordpress, html, autre
    facebook_page TEXT,  -- Nom/ID de la page Facebook
    twitter_account TEXT,  -- Nom du compte Twitter (sans @)
    actif BOOLEAN DEFAULT 1,
    derniere_collecte TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des articles
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id INTEGER NOT NULL,
    titre TEXT NOT NULL,
    contenu TEXT,
    extrait TEXT,
    url TEXT UNIQUE NOT NULL,
    auteur TEXT,
    date_publication TIMESTAMP,
    image_url TEXT,
    categories TEXT,  -- JSON array
    tags TEXT,  -- JSON array
    
    -- Métadonnées de scraping
    source_type TEXT NOT NULL,  -- wordpress_api, html_scraping
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Engagement
    vues INTEGER DEFAULT 0,
    commentaires INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (media_id) REFERENCES medias(id) ON DELETE CASCADE
);

-- Table des logs de scraping
CREATE TABLE IF NOT EXISTS scraping_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id INTEGER,
    status TEXT NOT NULL,  -- success, error, partial
    methode TEXT,  -- wordpress_api, html_scraping
    articles_collectes INTEGER DEFAULT 0,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (media_id) REFERENCES medias(id) ON DELETE CASCADE
);

-- Table des classifications thématiques
CREATE TABLE IF NOT EXISTS classifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL UNIQUE,
    categorie TEXT NOT NULL,  -- Politique, Économie, Sécurité, Santé, Culture, Sport, Autres
    confiance REAL NOT NULL,  -- Score de confiance (0-1)
    mots_cles TEXT,  -- JSON array des mots-clés
    justification TEXT,  -- Explication de la classification
    methode TEXT,  -- mistral_ollama, keywords_fallback
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);

-- Table des entités extraites (personnes, lieux, organisations)
CREATE TABLE IF NOT EXISTS entites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    type TEXT NOT NULL,  -- PERSON, LOCATION, ORGANIZATION
    valeur TEXT NOT NULL,
    contexte TEXT,  -- Phrase où l'entité apparaît
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);

-- Table des posts Facebook et leurs métriques
CREATE TABLE IF NOT EXISTS facebook_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id INTEGER NOT NULL,
    post_id TEXT UNIQUE NOT NULL,  -- ID Facebook du post
    message TEXT,
    url TEXT,
    image_url TEXT,
    date_publication TIMESTAMP,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    engagement_total INTEGER DEFAULT 0,  -- likes + comments + shares
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (media_id) REFERENCES medias(id) ON DELETE CASCADE
);

-- Table des tweets et leurs métriques
CREATE TABLE IF NOT EXISTS twitter_tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id INTEGER NOT NULL,
    tweet_id TEXT UNIQUE NOT NULL,  -- ID Twitter du tweet
    text TEXT,
    url TEXT,
    image_url TEXT,
    date_publication TIMESTAMP,
    retweets INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    quotes INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    engagement_total INTEGER DEFAULT 0,  -- retweets + replies + likes + quotes
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (media_id) REFERENCES medias(id) ON DELETE CASCADE
);

-- Table des métriques d'audience par média
CREATE TABLE IF NOT EXISTS media_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id INTEGER NOT NULL,
    periode_debut DATE NOT NULL,
    periode_fin DATE NOT NULL,
    
    -- Volume
    total_articles INTEGER DEFAULT 0,
    total_posts_facebook INTEGER DEFAULT 0,
    total_tweets INTEGER DEFAULT 0,
    
    -- Engagement Facebook
    total_likes_fb INTEGER DEFAULT 0,
    total_comments_fb INTEGER DEFAULT 0,
    total_shares_fb INTEGER DEFAULT 0,
    engagement_total_fb INTEGER DEFAULT 0,
    
    -- Engagement Twitter
    total_retweets INTEGER DEFAULT 0,
    total_replies INTEGER DEFAULT 0,
    total_likes_tw INTEGER DEFAULT 0,
    total_quotes INTEGER DEFAULT 0,
    total_impressions INTEGER DEFAULT 0,
    engagement_total_tw INTEGER DEFAULT 0,
    
    -- Engagement global
    engagement_total INTEGER DEFAULT 0,  -- Facebook + Twitter
    engagement_moyen REAL DEFAULT 0,
    
    -- Scores calculés
    score_volume REAL DEFAULT 0,  -- Basé sur nombre de publications
    score_engagement REAL DEFAULT 0,  -- Basé sur interactions sociales
    score_influence REAL DEFAULT 0,  -- Score composite final
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (media_id) REFERENCES medias(id) ON DELETE CASCADE
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_articles_media ON articles(media_id);
CREATE INDEX IF NOT EXISTS idx_articles_date ON articles(date_publication);
CREATE INDEX IF NOT EXISTS idx_articles_url ON articles(url);
CREATE INDEX IF NOT EXISTS idx_articles_scraped ON articles(scraped_at);
CREATE INDEX IF NOT EXISTS idx_medias_url ON medias(url);
CREATE INDEX IF NOT EXISTS idx_logs_media ON scraping_logs(media_id);
CREATE INDEX IF NOT EXISTS idx_logs_date ON scraping_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_classifications_article ON classifications(article_id);
CREATE INDEX IF NOT EXISTS idx_classifications_categorie ON classifications(categorie);
CREATE INDEX IF NOT EXISTS idx_entites_article ON entites(article_id);
CREATE INDEX IF NOT EXISTS idx_entites_type ON entites(type);
CREATE INDEX IF NOT EXISTS idx_facebook_posts_media ON facebook_posts(media_id);
CREATE INDEX IF NOT EXISTS idx_facebook_posts_date ON facebook_posts(date_publication);
CREATE INDEX IF NOT EXISTS idx_twitter_tweets_media ON twitter_tweets(media_id);
CREATE INDEX IF NOT EXISTS idx_twitter_tweets_date ON twitter_tweets(date_publication);
CREATE INDEX IF NOT EXISTS idx_media_metrics_media ON media_metrics(media_id);
CREATE INDEX IF NOT EXISTS idx_media_metrics_periode ON media_metrics(periode_debut, periode_fin);

-- ==================== TABLE: CONTENT_MODERATION ====================
-- Stocke les analyses de modération de contenu (détection de toxicité, fake news, etc.)
CREATE TABLE IF NOT EXISTS content_moderation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_type TEXT NOT NULL,  -- 'article', 'facebook_post', 'tweet'
    content_id INTEGER NOT NULL,  -- ID du contenu analysé
    
    -- Scores globaux
    risk_score REAL DEFAULT 0,  -- Score de risque global (0-10)
    risk_level TEXT,  -- Niveau de risque: MINIMAL, FAIBLE, MOYEN, ÉLEVÉ, CRITIQUE
    should_flag BOOLEAN DEFAULT 0,  -- Si le contenu doit être signalé
    
    -- Analyse de toxicité
    is_toxic BOOLEAN DEFAULT 0,
    toxicity_score REAL DEFAULT 0,
    hate_speech_score REAL DEFAULT 0,
    violence_score REAL DEFAULT 0,
    insults_score REAL DEFAULT 0,
    discrimination_score REAL DEFAULT 0,
    
    -- Analyse de désinformation
    is_misinformation BOOLEAN DEFAULT 0,
    misinformation_score REAL DEFAULT 0,
    unverified_claims_score REAL DEFAULT 0,
    fact_manipulation_score REAL DEFAULT 0,
    conspiracy_score REAL DEFAULT 0,
    propaganda_score REAL DEFAULT 0,
    suspicious_elements TEXT,  -- JSON array
    
    -- Analyse de sensibilité
    is_sensitive BOOLEAN DEFAULT 0,
    sensitivity_level TEXT,  -- faible, moyen, élevé, critique
    sensitivity_score REAL DEFAULT 0,
    sensitive_categories TEXT,  -- JSON array
    
    -- Métadonnées
    toxicity_reason TEXT,
    misinformation_reason TEXT,
    sensitivity_reason TEXT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_used TEXT DEFAULT 'llama3.2',
    
    UNIQUE(content_type, content_id)
);

CREATE INDEX IF NOT EXISTS idx_moderation_content ON content_moderation(content_type, content_id);
CREATE INDEX IF NOT EXISTS idx_moderation_risk ON content_moderation(risk_score DESC);
CREATE INDEX IF NOT EXISTS idx_moderation_flag ON content_moderation(should_flag);
CREATE INDEX IF NOT EXISTS idx_moderation_toxic ON content_moderation(is_toxic);
CREATE INDEX IF NOT EXISTS idx_moderation_misinfo ON content_moderation(is_misinformation);
