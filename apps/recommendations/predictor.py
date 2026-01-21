# Location: apps\recommendations\predictor.py
"""
NexCart Recommendation Predictor
Generate recommendations for users
"""
from pathlib import Path
from django.conf import settings
from .model import RecommendationEngine
import logging

logger = logging.getLogger(__name__)


class RecommendationPredictor:
    """Generate product recommendations"""
    
    def __init__(self):
        self.engine = None
        self.model_path = settings.ML_MODEL_PATH / 'recommendation_model.pkl'
        self._load_model()
    
    def _load_model(self):
        """Load trained model"""
        try:
            if self.model_path.exists():
                self.engine = RecommendationEngine()
                self.engine.load_model(self.model_path)
                logger.info("Recommendation model loaded successfully")
            else:
                logger.warning("No trained model found")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
    
    def get_recommendations_for_user(self, user_id, n_recommendations=10):
        """
        Get personalized recommendations for a user
        
        Args:
            user_id: User ID
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of product IDs
        """
        if not self.engine:
            logger.warning("Model not loaded, returning popular products")
            return self._get_popular_products(n_recommendations)
        
        try:
            recommendations = self.engine.get_hybrid_recommendations(
                user_id=str(user_id),
                n_recommendations=n_recommendations
            )
            
            logger.info(f"Generated {len(recommendations)} recommendations for user {user_id}")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._get_popular_products(n_recommendations)
    
    def get_similar_products(self, product_id, n_recommendations=10):
        """
        Get products similar to a given product
        
        Args:
            product_id: Product ID
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of (product_id, similarity_score) tuples
        """
        if not self.engine:
            logger.warning("Model not loaded")
            return []
        
        try:
            similar = self.engine.get_content_based_recommendations(
                product_id=str(product_id),
                n_recommendations=n_recommendations
            )
            
            logger.info(f"Found {len(similar)} similar products for {product_id}")
            return similar
            
        except Exception as e:
            logger.error(f"Error finding similar products: {str(e)}")
            return []
    
    def get_popular_products(self, n_recommendations=10):
        """
        Get popular products
        
        Args:
            n_recommendations: Number of products to return
            
        Returns:
            List of product IDs
        """
        return self._get_popular_products(n_recommendations)
    
    def _get_popular_products(self, n=10):
        """Fallback: Get popular products from database"""
        from apps.products.models import Product
        
        try:
            products = Product.objects.filter(
                is_active=True
            ).order_by('-purchase_count', '-view_count')[:n]
            
            return [str(p.id) for p in products]
            
        except Exception as e:
            logger.error(f"Error getting popular products: {str(e)}")
            return []
    
    def reload_model(self):
        """Reload model (used after retraining)"""
        self._load_model()