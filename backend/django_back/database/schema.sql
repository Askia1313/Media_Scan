-- Schéma de base de données SQLite pour MÉDIA-SCAN

-- Table des médias
CREATE TABLE IF NOT EXISTS medias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    type_site TEXT DEFAULT 'unknown',  -- wordpress, html, autre
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

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_articles_media ON articles(media_id);
CREATE INDEX IF NOT EXISTS idx_articles_date ON articles(date_publication);
CREATE INDEX IF NOT EXISTS idx_articles_url ON articles(url);
CREATE INDEX IF NOT EXISTS idx_articles_scraped ON articles(scraped_at);
CREATE INDEX IF NOT EXISTS idx_medias_url ON medias(url);
CREATE INDEX IF NOT EXISTS idx_logs_media ON scraping_logs(media_id);
CREATE INDEX IF NOT EXISTS idx_logs_date ON scraping_logs(created_at);
