# Location: apps\recommendations\services.py
"""
NexCart Recommendation Services
API services for recommendations
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.core.cache import cache

from apps.products.models import Product
from apps.products.serializers import ProductListSerializer
from .predictor import RecommendationPredictor
import logging

logger = logging.getLogger(__name__)

# Initialize predictor
predictor = RecommendationPredictor()


@api_view(['GET'])
@permission_classes([AllowAny])
def get_recommendations(request):
    """Get personalized recommendations for authenticated user or popular products"""
    try:
        n_recommendations = int(request.GET.get('n', 10))
        
        if request.user.is_authenticated:
            # Get personalized recommendations
            cache_key = f'recommendations_{request.user.id}'
            product_ids = cache.get(cache_key)
            
            if not product_ids:
                product_ids = predictor.get_recommendations_for_user(
                    user_id=str(request.user.id),
                    n_recommendations=n_recommendations
                )
                # Cache for 1 hour
                cache.set(cache_key, product_ids, 3600)
        else:
            # Get popular products for anonymous users
            cache_key = 'popular_products'
            product_ids = cache.get(cache_key)
            
            if not product_ids:
                product_ids = predictor.get_popular_products(n_recommendations)
                # Cache for 1 hour
                cache.set(cache_key, product_ids, 3600)
        
        # Fetch products
        products = Product.objects.filter(
            id__in=product_ids,
            is_active=True
        )
        
        # Preserve order from recommendations
        products_dict = {str(p.id): p for p in products}
        ordered_products = [products_dict[pid] for pid in product_ids if pid in products_dict]
        
        serializer = ProductListSerializer(ordered_products, many=True)
        
        return Response({
            'results': serializer.data,
            'count': len(serializer.data)
        })
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return Response({
            'error': 'Failed to get recommendations'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_similar_products(request, product_id):
    """Get products similar to a given product"""
    try:
        n_recommendations = int(request.GET.get('n', 10))
        
        # Check if product exists
        try:
            Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get similar products
        cache_key = f'similar_{product_id}'
        similar = cache.get(cache_key)
        
        if not similar:
            similar = predictor.get_similar_products(
                product_id=product_id,
                n_recommendations=n_recommendations
            )
            # Cache for 6 hours
            cache.set(cache_key, similar, 21600)
        
        # Extract product IDs
        product_ids = [pid for pid, _ in similar]
        
        # Fetch products
        products = Product.objects.filter(
            id__in=product_ids,
            is_active=True
        )
        
        # Preserve order and include similarity scores
        products_dict = {str(p.id): p for p in products}
        results = []
        
        for pid, score in similar:
            if pid in products_dict:
                product_data = ProductListSerializer(products_dict[pid]).data
                product_data['similarity_score'] = float(score)
                results.append(product_data)
        
        return Response({
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error getting similar products: {str(e)}")
        return Response({
            'error': 'Failed to get similar products'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def retrain_model(request):
    """Manually trigger model retraining (admin only)"""
    try:
        if not request.user.is_staff:
            return Response({
                'error': 'Permission denied'
            }, status=status.HTTP_403_FORBIDDEN)
        
        from .trainer import RecommendationTrainer
        from celery import shared_task
        
        # Trigger async training
        @shared_task
        def train_async():
            trainer = RecommendationTrainer()
            trainer.train()
            predictor.reload_model()
        
        train_async.delay()
        
        return Response({
            'message': 'Model retraining started'
        })
        
    except Exception as e:
        logger.error(f"Error triggering retraining: {str(e)}")
        return Response({
            'error': 'Failed to trigger retraining'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)