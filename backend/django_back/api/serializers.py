"""
Serializers pour l'API REST
"""

from rest_framework import serializers
from datetime import datetime, timedelta


class MediaSerializer(serializers.Serializer):
    """Serializer pour les médias"""
    id = serializers.IntegerField(read_only=True)
    nom = serializers.CharField(max_length=200)
    url = serializers.URLField()
    type_site = serializers.CharField(max_length=50, required=False)
    facebook_page = serializers.CharField(max_length=100, required=False, allow_null=True)
    twitter_account = serializers.CharField(max_length=100, required=False, allow_null=True)
    actif = serializers.BooleanField(default=True)
    derniere_collecte = serializers.DateTimeField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)


class ArticleSerializer(serializers.Serializer):
    """Serializer pour les articles"""
    id = serializers.IntegerField(read_only=True)
    media_id = serializers.IntegerField()
    titre = serializers.CharField()
    contenu = serializers.CharField(required=False, allow_null=True)
    extrait = serializers.CharField(required=False, allow_null=True)
    url = serializers.URLField()
    auteur = serializers.CharField(required=False, allow_null=True)
    date_publication = serializers.DateTimeField(required=False, allow_null=True)
    image_url = serializers.URLField(required=False, allow_null=True)
    categories = serializers.ListField(required=False)
    tags = serializers.ListField(required=False)
    source_type = serializers.CharField()
    vues = serializers.IntegerField(default=0)
    commentaires = serializers.IntegerField(default=0)
    scraped_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class ClassificationSerializer(serializers.Serializer):
    """Serializer pour les classifications thématiques"""
    id = serializers.IntegerField(read_only=True)
    article_id = serializers.IntegerField()
    categorie = serializers.CharField()
    confiance = serializers.FloatField()
    mots_cles = serializers.ListField(required=False)
    justification = serializers.CharField(required=False, allow_null=True)
    methode = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)


class FacebookPostSerializer(serializers.Serializer):
    """Serializer pour les posts Facebook"""
    id = serializers.IntegerField(read_only=True)
    media_id = serializers.IntegerField()
    post_id = serializers.CharField()
    message = serializers.CharField(required=False, allow_null=True)
    url = serializers.URLField(required=False, allow_null=True)
    image_url = serializers.URLField(required=False, allow_null=True)
    date_publication = serializers.DateTimeField(required=False, allow_null=True)
    likes = serializers.IntegerField(default=0)
    comments = serializers.IntegerField(default=0)
    shares = serializers.IntegerField(default=0)
    engagement_total = serializers.IntegerField(default=0)
    scraped_at = serializers.DateTimeField(read_only=True)


class TwitterTweetSerializer(serializers.Serializer):
    """Serializer pour les tweets"""
    id = serializers.IntegerField(read_only=True)
    media_id = serializers.IntegerField()
    tweet_id = serializers.CharField()
    text = serializers.CharField(required=False, allow_null=True)
    url = serializers.URLField(required=False, allow_null=True)
    image_url = serializers.URLField(required=False, allow_null=True)
    date_publication = serializers.DateTimeField(required=False, allow_null=True)
    retweets = serializers.IntegerField(default=0)
    replies = serializers.IntegerField(default=0)
    likes = serializers.IntegerField(default=0)
    quotes = serializers.IntegerField(default=0)
    impressions = serializers.IntegerField(default=0)
    engagement_total = serializers.IntegerField(default=0)
    scraped_at = serializers.DateTimeField(read_only=True)


class AudienceWebSerializer(serializers.Serializer):
    """Serializer pour l'audience web"""
    id = serializers.IntegerField()
    nom = serializers.CharField()
    url = serializers.URLField()
    total_articles = serializers.IntegerField()
    jours_avec_publication = serializers.IntegerField()
    articles_par_jour_moyen = serializers.FloatField()
    derniere_publication = serializers.DateTimeField(allow_null=True)
    jours_depuis_derniere_pub = serializers.IntegerField()
    statut = serializers.CharField()


class AudienceFacebookSerializer(serializers.Serializer):
    """Serializer pour l'audience Facebook"""
    id = serializers.IntegerField()
    nom = serializers.CharField()
    url = serializers.URLField()
    facebook_page = serializers.CharField()
    total_posts = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    total_shares = serializers.IntegerField()
    engagement_total = serializers.IntegerField()
    engagement_moyen = serializers.FloatField()
    jours_avec_publication = serializers.IntegerField()
    posts_par_jour_moyen = serializers.FloatField()
    derniere_publication = serializers.DateTimeField(allow_null=True)
    jours_depuis_derniere_pub = serializers.IntegerField()
    statut = serializers.CharField()


class AudienceTwitterSerializer(serializers.Serializer):
    """Serializer pour l'audience Twitter"""
    id = serializers.IntegerField()
    nom = serializers.CharField()
    url = serializers.URLField()
    twitter_account = serializers.CharField()
    total_tweets = serializers.IntegerField()
    total_retweets = serializers.IntegerField()
    total_replies = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    total_quotes = serializers.IntegerField()
    total_impressions = serializers.IntegerField()
    engagement_total = serializers.IntegerField()
    engagement_moyen = serializers.FloatField()
    jours_avec_publication = serializers.IntegerField()
    tweets_par_jour_moyen = serializers.FloatField()
    derniere_publication = serializers.DateTimeField(allow_null=True)
    jours_depuis_derniere_pub = serializers.IntegerField()
    statut = serializers.CharField()


class AudienceGlobalSerializer(serializers.Serializer):
    """Serializer pour l'audience globale"""
    id = serializers.IntegerField()
    nom = serializers.CharField()
    url = serializers.URLField()
    total_publications = serializers.IntegerField()
    total_engagement = serializers.IntegerField()
    score_influence = serializers.FloatField()
    web = AudienceWebSerializer(required=False)
    facebook = AudienceFacebookSerializer(required=False)
    twitter = AudienceTwitterSerializer(required=False)


class CategoryStatsSerializer(serializers.Serializer):
    """Serializer pour les statistiques par catégorie"""
    categorie = serializers.CharField()
    total = serializers.IntegerField()
    confiance_moyenne = serializers.FloatField()


class MediaRankingSerializer(serializers.Serializer):
    """Serializer pour le classement des médias"""
    id = serializers.IntegerField()
    nom = serializers.CharField()
    url = serializers.URLField()
    total_articles = serializers.IntegerField()
    total_posts_facebook = serializers.IntegerField()
    total_tweets = serializers.IntegerField()
    total_likes_fb = serializers.IntegerField()
    total_comments_fb = serializers.IntegerField()
    total_shares_fb = serializers.IntegerField()
    engagement_total_fb = serializers.IntegerField()
    total_retweets = serializers.IntegerField()
    total_replies = serializers.IntegerField()
    total_likes_tw = serializers.IntegerField()
    total_quotes = serializers.IntegerField()
    total_impressions = serializers.IntegerField()
    engagement_total_tw = serializers.IntegerField()
    engagement_total = serializers.IntegerField()
    engagement_moyen = serializers.FloatField()


class ScrapingRequestSerializer(serializers.Serializer):
    """Serializer pour les requêtes de scraping"""
    url = serializers.URLField(required=False)
    all = serializers.BooleanField(default=False)
    days = serializers.IntegerField(default=30)
    fb_posts = serializers.IntegerField(default=5)
    tweets = serializers.IntegerField(default=5)
    skip_facebook = serializers.BooleanField(default=False)
    skip_twitter = serializers.BooleanField(default=False)


class ScrapingResponseSerializer(serializers.Serializer):
    """Serializer pour les réponses de scraping"""
    status = serializers.CharField()
    message = serializers.CharField()
    total_articles = serializers.IntegerField(required=False)
    total_fb_posts = serializers.IntegerField(required=False)
    total_tweets = serializers.IntegerField(required=False)
    errors = serializers.ListField(required=False)
