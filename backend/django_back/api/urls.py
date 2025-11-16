"""
URLs pour l'API REST
"""

from django.urls import path
from .views import (
    # Médias
    MediaListView, MediaDetailView,
    # Articles
    ArticleListView,
    # Classifications
    ClassificationListView, CategoryStatsView,
    # Facebook
    FacebookPostListView,
    # Twitter
    TwitterTweetListView,
    # Audience
    AudienceWebView, AudienceFacebookView, AudienceTwitterView,
    AudienceGlobalView, InactiveMediasView,
    # Ranking
    MediaRankingView,
    # Scraping
    ScrapingTriggerView,
    # Stats
    stats_overview, health_check
)

urlpatterns = [
    # Health check
    path('health/', health_check, name='health-check'),
    
    # Médias
    path('medias/', MediaListView.as_view(), name='media-list'),
    path('medias/<int:media_id>/', MediaDetailView.as_view(), name='media-detail'),
    
    # Articles
    path('articles/', ArticleListView.as_view(), name='article-list'),
    
    # Classifications
    path('classifications/', ClassificationListView.as_view(), name='classification-list'),
    path('classifications/stats/', CategoryStatsView.as_view(), name='category-stats'),
    
    # Facebook
    path('facebook/posts/', FacebookPostListView.as_view(), name='facebook-posts'),
    
    # Twitter
    path('twitter/tweets/', TwitterTweetListView.as_view(), name='twitter-tweets'),
    
    # Audience
    path('audience/web/', AudienceWebView.as_view(), name='audience-web'),
    path('audience/facebook/', AudienceFacebookView.as_view(), name='audience-facebook'),
    path('audience/twitter/', AudienceTwitterView.as_view(), name='audience-twitter'),
    path('audience/global/', AudienceGlobalView.as_view(), name='audience-global'),
    path('audience/inactive/', InactiveMediasView.as_view(), name='inactive-medias'),
    
    # Ranking
    path('ranking/', MediaRankingView.as_view(), name='media-ranking'),
    
    # Scraping
    path('scraping/trigger/', ScrapingTriggerView.as_view(), name='scraping-trigger'),
    
    # Stats
    path('stats/', stats_overview, name='stats-overview'),
]
