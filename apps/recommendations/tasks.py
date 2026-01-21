"""
NexCart Recommendation Celery Tasks
"""
from celery import shared_task
from .trainer import RecommendationTrainer
from .predictor import RecommendationPredictor
import logging

logger = logging.getLogger(__name__)


@shared_task
def retrain_recommendation_model():
    """
    Periodic task to retrain recommendation model
    Runs daily at 2 AM
    """
    logger.info("Starting scheduled recommendation model retraining...")
    
    try:
        trainer = RecommendationTrainer()
        success = trainer.train(n_components=50)
        
        if success:
            # Reload model in predictor
            predictor = RecommendationPredictor()
            predictor.reload_model()
            
            logger.info("Recommendation model retrained successfully")
            return {'status': 'success', 'message': 'Model retrained'}
        else:
            logger.error("Model retraining failed")
            return {'status': 'failed', 'message': 'Insufficient data or training error'}
            
    except Exception as e:
        logger.error(f"Error in scheduled retraining: {str(e)}")
        return {'status': 'error', 'message': str(e)}