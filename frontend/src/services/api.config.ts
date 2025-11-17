/**
 * Configuration de l'API
 */

export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  TIMEOUT: 30000,
  HEADERS: {
    'Content-Type': 'application/json',
  },
};

export const API_ENDPOINTS = {
  // Health
  HEALTH: '/api/health/',
  
  // Médias
  MEDIAS: '/api/medias/',
  MEDIA_DETAIL: (id: number) => `/api/medias/${id}/`,
  
  // Articles
  ARTICLES: '/api/articles/',
  
  // Classifications
  CLASSIFICATIONS: '/api/classifications/',
  CLASSIFICATIONS_STATS: '/api/classifications/stats/',
  CLASSIFICATIONS_WEEKLY: '/api/classifications/weekly/',
  
  // Facebook
  FACEBOOK_POSTS: '/api/facebook/posts/',
  
  // Twitter
  TWITTER_TWEETS: '/api/twitter/tweets/',
  
  // Audience
  AUDIENCE_WEB: '/api/audience/web/',
  AUDIENCE_FACEBOOK: '/api/audience/facebook/',
  AUDIENCE_TWITTER: '/api/audience/twitter/',
  AUDIENCE_GLOBAL: '/api/audience/global/',
  AUDIENCE_INACTIVE: '/api/audience/inactive/',
  
  // Classement
  RANKING: '/api/ranking/',
  
  // Scraping
  SCRAPING_TRIGGER: '/api/scraping/trigger/',
  SCRAPING_SCHEDULE: '/api/scraping/schedule/',
  SCRAPING_SCHEDULE_DETAIL: (id: number) => `/api/scraping/schedule/${id}/`,
  
  // Statistiques
  STATS: '/api/stats/',
} as const;
