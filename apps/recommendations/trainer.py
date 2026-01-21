# Location: apps\recommendations\trainer.py
"""
NexCart Recommendation Model Trainer
Train and update recommendation models
"""
import logging
from pathlib import Path
from django.conf import settings
from .data_loader import load_training_data
from .model import RecommendationEngine

logger = logging.getLogger(__name__)


class RecommendationTrainer:
    """Train recommendation models"""
    
    def __init__(self):
        self.model_path = settings.ML_MODEL_PATH
        self.model_path.mkdir(parents=True, exist_ok=True)
    
    def train(self, n_components=50):
        """
        Train recommendation model
        
        Args:
            n_components: Number of latent factors for SVD
        """
        logger.info("Starting recommendation model training...")
        
        try:
            # Load training data
            logger.info("Loading training data...")
            interactions_df, products_df = load_training_data()
            
            if interactions_df.empty:
                logger.warning("No interaction data available for training")
                return False
            
            logger.info(f"Loaded {len(interactions_df)} interactions and {len(products_df)} products")
            
            # Initialize engine
            engine = RecommendationEngine()
            
            # Prepare data
            logger.info("Preparing data...")
            engine.prepare_data(interactions_df, products_df)
            
            # Train collaborative filtering
            logger.info("Training collaborative filtering model...")
            engine.train_collaborative_filtering(n_components=n_components)
            
            # Train content-based filtering
            logger.info("Training content-based filtering model...")
            engine.train_content_based()
            
            # Save model
            model_file = self.model_path / 'recommendation_model.pkl'
            logger.info(f"Saving model to {model_file}...")
            engine.save_model(model_file)
            
            logger.info("Model training completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Model training failed: {str(e)}")
            return False
    
    def evaluate(self):
        """
        Evaluate model performance
        
        Returns:
            Dictionary of evaluation metrics
        """
        logger.info("Evaluating model performance...")
        
        try:
            # Load model
            model_file = self.model_path / 'recommendation_model.pkl'
            if not model_file.exists():
                logger.error("No trained model found")
                return None
            
            engine = RecommendationEngine()
            engine.load_model(model_file)
            
            # Load test data
            interactions_df, _ = load_training_data()
            
            # Simple evaluation: check if model can generate recommendations
            sample_users = interactions_df['user_id'].unique()[:10]
            
            successful_recommendations = 0
            for user_id in sample_users:
                recs = engine.get_hybrid_recommendations(str(user_id), n_recommendations=10)
                if len(recs) > 0:
                    successful_recommendations += 1
            
            metrics = {
                'total_users_tested': len(sample_users),
                'successful_recommendations': successful_recommendations,
                'success_rate': successful_recommendations / len(sample_users) if sample_users else 0
            }
            
            logger.info(f"Evaluation metrics: {metrics}")
            return metrics
            
        except Exception as e:
            logger.error(f"Model evaluation failed: {str(e)}")
            return None 