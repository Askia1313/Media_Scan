/**
 * Types TypeScript pour les données de l'API
 */

// Médias
export interface Media {
  id: number;
  nom: string;
  url: string;
  type_site: string;
  facebook_page?: string;
  twitter_account?: string;
  actif: boolean;
  derniere_collecte?: string;
  created_at: string;
}

// Articles
export interface Article {
  id: number;
  media_id: number;
  titre: string;
  contenu: string;
  extrait: string;
  url: string;
  auteur?: string;
  date_publication: string;
  image_url?: string;
  categories: string[];
  tags: string[];
  source_type: string;
  vues: number;
  commentaires: number;
  scraped_at: string;
  created_at: string;
}

// Classifications
export interface Classification {
  id: number;
  article_id: number;
  categorie: string;
  score_confiance: number;
  created_at: string;
}

export interface ClassificationStats {
  categorie: string;
  total: number;
  confiance_moyenne: number;
}

export interface WeeklyCategoryStats {
  semaine: string;
  categorie: string;
  total: number;
}

// Facebook
export interface FacebookPost {
  id: number;
  media_id: number;
  post_id: string;
  message: string;
  url: string;
  image_url?: string;
  date_publication: string;
  likes: number;
  comments: number;
  shares: number;
  engagement_total: number;
  scraped_at: string;
}

// Twitter
export interface Tweet {
  id: number;
  media_id: number;
  tweet_id: string;
  text: string;
  url: string;
  image_url?: string;
  date_publication: string;
  retweets: number;
  replies: number;
  likes: number;
  quotes: number;
  impressions: number;
  engagement_total: number;
  scraped_at: string;
}

// Audience
export interface AudienceWeb {
  id: number;
  nom: string;
  url: string;
  total_articles: number;
  jours_avec_publication: number;
  articles_par_jour_moyen: number;
  derniere_publication?: string;
  jours_depuis_derniere_pub: number;
  statut: string;
}

export interface AudienceFacebook {
  id: number;
  nom: string;
  url: string;
  facebook_page?: string;
  total_posts: number;
  total_likes: number;
  total_comments: number;
  total_shares: number;
  engagement_total: number;
  engagement_moyen: number;
  jours_avec_publication: number;
  posts_par_jour_moyen: number;
  derniere_publication?: string;
  jours_depuis_derniere_pub: number;
  statut: string;
}

export interface AudienceTwitter {
  id: number;
  nom: string;
  url: string;
  twitter_account?: string;
  total_tweets: number;
  total_retweets: number;
  total_replies: number;
  total_likes: number;
  total_quotes: number;
  total_impressions: number;
  engagement_total: number;
  engagement_moyen: number;
  jours_avec_publication: number;
  tweets_par_jour_moyen: number;
  derniere_publication?: string;
  jours_depuis_derniere_pub: number;
  statut: string;
}

export interface AudienceGlobal {
  id: number;
  nom: string;
  url: string;
  total_publications: number;
  total_engagement: number;
  score_influence: number;
  web?: AudienceWeb;
  facebook?: AudienceFacebook;
  twitter?: AudienceTwitter;
}

export interface InactiveMedia {
  nom: string;
  jours_depuis_derniere_pub: number;
}

export interface InactiveMedias {
  web: InactiveMedia[];
  facebook: InactiveMedia[];
  twitter: InactiveMedia[];
}

// Classement
export interface Ranking {
  id: number;
  nom: string;
  url: string;
  total_articles: number;
  total_posts_facebook: number;
  total_tweets: number;
  total_likes_fb: number;
  total_comments_fb: number;
  total_shares_fb: number;
  engagement_total_fb: number;
  total_retweets: number;
  total_replies: number;
  total_likes_tw: number;
  total_quotes: number;
  total_impressions: number;
  engagement_total_tw: number;
  engagement_total: number;
  engagement_moyen: number;
}

// Scraping
export interface ScrapingRequest {
  url?: string;
  all?: boolean;
  days?: number;
  fb_posts?: number;
  tweets?: number;
  skip_facebook?: boolean;
  skip_twitter?: boolean;
}

export interface ScrapingResponse {
  status: string;
  message: string;
  total_articles: number;
  total_fb_posts: number;
  total_tweets: number;
}

// Statistiques
export interface Stats {
  total_medias: number;
  total_articles: number;
  total_categories: number;
  top_media: {
    nom: string;
    engagement_total: number;
  };
  period_days: number;
}

// Health
export interface HealthCheck {
  status: string;
  database: string;
  version: string;
}
