"""
Views pour l'API REST - Media Scanner
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse

import sys
import os

# Ajouter le chemin parent pour importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from analysis.audience_analyzer import AudienceAnalyzer
from .serializers import (
    MediaSerializer, ArticleSerializer, ClassificationSerializer,
    FacebookPostSerializer, TwitterTweetSerializer,
    AudienceWebSerializer, AudienceFacebookSerializer, AudienceTwitterSerializer,
    AudienceGlobalSerializer, CategoryStatsSerializer, WeeklyCategoryStatsSerializer,
    MediaRankingSerializer, ScrapingRequestSerializer, ScrapingResponseSerializer
)


# Initialiser le gestionnaire de base de données
db = DatabaseManager()
analyzer = AudienceAnalyzer(db)


# ==================== MÉDIAS ====================

class MediaListView(APIView):
    """Liste tous les médias"""
    
    def get(self, request):
        """GET /api/medias/?actif=true"""
        actif_only = request.GET.get('actif', 'false').lower() == 'true'
        medias = db.get_all_medias(actif_only=actif_only)
        serializer = MediaSerializer([{
            'id': m.id,
            'nom': m.nom,
            'url': m.url,
            'type_site': m.type_site,
            'facebook_page': m.facebook_page,
            'twitter_account': m.twitter_account,
            'actif': m.actif,
            'derniere_collecte': m.derniere_collecte,
            'created_at': m.created_at
        } for m in medias], many=True)
        
        return Response(serializer.data)
    
    def post(self, request):
        """POST /api/medias/ - Créer un nouveau média"""
        serializer = MediaSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            media_id = db.add_media(
                nom=serializer.validated_data['nom'],
                url=serializer.validated_data['url'],
                type_site=serializer.validated_data.get('type_site', 'unknown'),
                facebook_page=serializer.validated_data.get('facebook_page'),
                twitter_account=serializer.validated_data.get('twitter_account')
            )
            
            # Récupérer le média créé
            media = db.get_media_by_url(serializer.validated_data['url'])
            
            response_data = {
                'id': media.id,
                'nom': media.nom,
                'url': media.url,
                'type_site': media.type_site,
                'facebook_page': media.facebook_page,
                'twitter_account': media.twitter_account,
                'actif': media.actif,
                'derniere_collecte': media.derniere_collecte,
                'created_at': media.created_at
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MediaDetailView(APIView):
    """Détails d'un média"""
    
    def get(self, request, media_id):
        """GET /api/medias/{id}/"""
        # Récupérer le média par son ID
        medias = db.get_all_medias(actif_only=False)
        media = next((m for m in medias if m.id == media_id), None)
        
        if not media:
            return Response(
                {'error': 'Média non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = MediaSerializer({
            'id': media.id,
            'nom': media.nom,
            'url': media.url,
            'type_site': media.type_site,
            'facebook_page': media.facebook_page,
            'twitter_account': media.twitter_account,
            'actif': media.actif,
            'derniere_collecte': media.derniere_collecte,
            'created_at': media.created_at
        })
        
        return Response(serializer.data)
    
    def put(self, request, media_id):
        """PUT /api/medias/{id}/ - Mettre à jour un média"""
        # Vérifier que le média existe
        medias = db.get_all_medias(actif_only=False)
        media = next((m for m in medias if m.id == media_id), None)
        
        if not media:
            return Response(
                {'error': 'Média non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = MediaSerializer(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Mettre à jour le média
            conn = db.get_connection()
            cursor = conn.cursor()
            
            update_fields = []
            params = []
            
            if 'nom' in serializer.validated_data:
                update_fields.append('nom = ?')
                params.append(serializer.validated_data['nom'])
            
            if 'url' in serializer.validated_data:
                update_fields.append('url = ?')
                params.append(serializer.validated_data['url'])
            
            if 'type_site' in serializer.validated_data:
                update_fields.append('type_site = ?')
                params.append(serializer.validated_data['type_site'])
            
            if 'facebook_page' in serializer.validated_data:
                update_fields.append('facebook_page = ?')
                params.append(serializer.validated_data['facebook_page'])
            
            if 'twitter_account' in serializer.validated_data:
                update_fields.append('twitter_account = ?')
                params.append(serializer.validated_data['twitter_account'])
            
            if 'actif' in serializer.validated_data:
                update_fields.append('actif = ?')
                params.append(serializer.validated_data['actif'])
            
            if update_fields:
                params.append(media_id)
                query = f"UPDATE medias SET {', '.join(update_fields)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
            
            conn.close()
            
            # Récupérer le média mis à jour
            medias = db.get_all_medias(actif_only=False)
            updated_media = next((m for m in medias if m.id == media_id), None)
            
            response_data = {
                'id': updated_media.id,
                'nom': updated_media.nom,
                'url': updated_media.url,
                'type_site': updated_media.type_site,
                'facebook_page': updated_media.facebook_page,
                'twitter_account': updated_media.twitter_account,
                'actif': updated_media.actif,
                'derniere_collecte': updated_media.derniere_collecte,
                'created_at': updated_media.created_at
            }
            
            return Response(response_data)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, media_id):
        """DELETE /api/medias/{id}/ - Supprimer un média"""
        # Vérifier que le média existe
        medias = db.get_all_medias(actif_only=False)
        media = next((m for m in medias if m.id == media_id), None)
        
        if not media:
            return Response(
                {'error': 'Média non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM medias WHERE id = ?', (media_id,))
            conn.commit()
            conn.close()
            
            return Response(
                {'message': 'Média supprimé avec succès'},
                status=status.HTTP_204_NO_CONTENT
            )
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================== ARTICLES ====================

class ArticleListView(APIView):
    """Liste des articles"""
    
    def get(self, request):
        """GET /api/articles/?media_id=X&limit=100"""
        media_id = request.GET.get('media_id')
        limit = int(request.GET.get('limit', 100))
        days = int(request.GET.get('days', 7))
        
        if media_id:
            articles = db.get_articles_by_media(int(media_id), limit=limit)
        else:
            articles = db.get_recent_articles(days=days, limit=limit)
        
        serializer = ArticleSerializer([{
            'id': a.id,
            'media_id': a.media_id,
            'titre': a.titre,
            'contenu': a.contenu,
            'extrait': a.extrait,
            'url': a.url,
            'auteur': a.auteur,
            'date_publication': a.date_publication,
            'image_url': a.image_url,
            'categories': a.categories,
            'tags': a.tags,
            'source_type': a.source_type,
            'vues': a.vues,
            'commentaires': a.commentaires,
            'scraped_at': a.scraped_at,
            'created_at': a.created_at
        } for a in articles], many=True)
        
        return Response(serializer.data)


# ==================== CLASSIFICATIONS ====================

class ClassificationListView(APIView):
    """Liste des classifications"""
    
    def get(self, request):
        """GET /api/classifications/?categorie=Politique&limit=100"""
        categorie = request.GET.get('categorie')
        limit = int(request.GET.get('limit', 100))
        
        if categorie:
            results = db.get_articles_by_category(categorie, limit=limit)
            data = [{
                'article_id': r['article'].id,
                'categorie': r['categorie'],
                'confiance': r['confiance']
            } for r in results]
        else:
            data = []
        
        return Response(data)


class CategoryStatsView(APIView):
    """Statistiques par catégorie"""
    
    def get(self, request):
        """GET /api/classifications/stats/?days=30"""
        days = int(request.GET.get('days', 30))
        stats = db.get_category_stats(days=days)
        serializer = CategoryStatsSerializer(stats, many=True)
        return Response(serializer.data)


class WeeklyCategoryStatsView(APIView):
    """Statistiques hebdomadaires par catégorie"""
    
    def get(self, request):
        """GET /api/classifications/weekly/?weeks=5"""
        weeks = int(request.GET.get('weeks', 5))
        stats = db.get_weekly_category_stats(weeks=weeks)
        serializer = WeeklyCategoryStatsSerializer(stats, many=True)
        return Response(serializer.data)


# ==================== FACEBOOK ====================

class FacebookPostListView(APIView):
    """Liste des posts Facebook"""
    
    def get(self, request):
        """GET /api/facebook/posts/?media_id=X&limit=100"""
        media_id = request.GET.get('media_id')
        limit = int(request.GET.get('limit', 100))
        
        if not media_id:
            return Response(
                {'error': 'media_id requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        posts = db.get_facebook_posts_by_media(int(media_id), limit=limit)
        serializer = FacebookPostSerializer(posts, many=True)
        return Response(serializer.data)


# ==================== TWITTER ====================

class TwitterTweetListView(APIView):
    """Liste des tweets"""
    
    def get(self, request):
        """GET /api/twitter/tweets/?media_id=X&limit=100"""
        media_id = request.GET.get('media_id')
        limit = int(request.GET.get('limit', 100))
        
        if not media_id:
            return Response(
                {'error': 'media_id requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tweets = db.get_twitter_tweets_by_media(int(media_id), limit=limit)
        serializer = TwitterTweetSerializer(tweets, many=True)
        return Response(serializer.data)


# ==================== AUDIENCE ====================

class AudienceWebView(APIView):
    """Audience Web"""
    
    def get(self, request):
        """GET /api/audience/web/?days=30"""
        days = int(request.GET.get('days', 30))
        data = analyzer.analyze_web_audience(days=days)
        serializer = AudienceWebSerializer(data, many=True)
        return Response(serializer.data)


class AudienceFacebookView(APIView):
    """Audience Facebook"""
    
    def get(self, request):
        """GET /api/audience/facebook/?days=30"""
        days = int(request.GET.get('days', 30))
        data = analyzer.analyze_facebook_audience(days=days)
        serializer = AudienceFacebookSerializer(data, many=True)
        return Response(serializer.data)


class AudienceTwitterView(APIView):
    """Audience Twitter"""
    
    def get(self, request):
        """GET /api/audience/twitter/?days=30"""
        days = int(request.GET.get('days', 30))
        data = analyzer.analyze_twitter_audience(days=days)
        serializer = AudienceTwitterSerializer(data, many=True)
        return Response(serializer.data)


class AudienceGlobalView(APIView):
    """Audience globale"""
    
    def get(self, request):
        """GET /api/audience/global/?days=30"""
        days = int(request.GET.get('days', 30))
        data = analyzer.analyze_global_audience(days=days)
        serializer = AudienceGlobalSerializer(data, many=True)
        return Response(serializer.data)


class InactiveMediasView(APIView):
    """Médias inactifs"""
    
    def get(self, request):
        """GET /api/audience/inactive/?days_threshold=7"""
        days_threshold = int(request.GET.get('days_threshold', 7))
        data = analyzer.get_inactive_medias(days_threshold=days_threshold)
        return Response(data)


# ==================== RANKING ====================

class MediaRankingView(APIView):
    """Classement des médias"""
    
    def get(self, request):
        """GET /api/ranking/?days=30"""
        days = int(request.GET.get('days', 30))
        data = db.get_media_ranking_with_twitter(days=days)
        serializer = MediaRankingSerializer(data, many=True)
        return Response(serializer.data)


# ==================== SCRAPING ====================

class ScrapingTriggerView(APIView):
    """Déclencher un scraping"""
    
    def post(self, request):
        """POST /api/scraping/trigger/"""
        serializer = ScrapingRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: Implémenter le scraping asynchrone
        response_data = {
            'status': 'queued',
            'message': 'Scraping en cours...',
            'total_articles': 0,
            'total_fb_posts': 0,
            'total_tweets': 0
        }
        
        response_serializer = ScrapingResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)


# ==================== STATS ====================

@api_view(['GET'])
def stats_overview(request):
    """Vue d'ensemble des statistiques"""
    days = int(request.GET.get('days', 30))
    
    # Compter les médias
    medias = db.get_all_medias()
    
    # Compter les articles récents
    articles = db.get_recent_articles(days=days, limit=10000)
    
    # Statistiques par catégorie
    category_stats = db.get_category_stats(days=days)
    
    # Classement
    ranking = db.get_media_ranking_with_twitter(days=days)
    
    stats = {
        'total_medias': len(medias),
        'total_articles': len(articles),
        'total_categories': len(category_stats),
        'top_media': ranking[0] if ranking else None,
        'period_days': days
    }
    
    return Response(stats)


# ==================== MODÉRATION ====================

class ModerationStatsView(APIView):
    """Statistiques de modération"""
    
    def get(self, request):
        """GET /api/moderation/stats/"""
        stats = db.get_moderation_stats()
        return Response(stats)


class FlaggedContentListView(APIView):
    """Liste des contenus signalés"""
    
    def get(self, request):
        """GET /api/moderation/flagged/?content_type=article&limit=50"""
        content_type = request.GET.get('content_type')
        limit = int(request.GET.get('limit', 50))
        
        flagged = db.get_flagged_contents(content_type=content_type, limit=limit)
        return Response(flagged)


class ContentModerationView(APIView):
    """Détails de modération d'un contenu"""
    
    def get(self, request):
        """GET /api/moderation/content/?type=article&id=123"""
        content_type = request.GET.get('type')
        content_id = request.GET.get('id')
        
        if not content_type or not content_id:
            return Response(
                {'error': 'type et id requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            content_id = int(content_id)
            moderation = db.get_content_moderation(content_type, content_id)
            
            if moderation:
                return Response(moderation)
            else:
                return Response(
                    {'error': 'Contenu non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except ValueError:
            return Response(
                {'error': 'ID invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET'])
def health_check(request):
    """Vérification de l'état de l'API"""
    return Response({
        'status': 'healthy',
        'database': 'connected',
        'version': '1.0.0'
    })
