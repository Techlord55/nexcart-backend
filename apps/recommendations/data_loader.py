# Location: apps\recommendations\data_loader.py
"""
NexCart Recommendation Data Loader
Load and prepare data for ML training
"""
import pandas as pd
from django.db.models import Q
from apps.users.models import UserActivity
from apps.products.models import Product
import logging

logger = logging.getLogger(__name__)


def load_training_data():
    """
    Load training data from database
    
    Returns:
        Tuple of (interactions_df, products_df)
    """
    logger.info("Loading training data from database...")
    
    # Load user interactions
    interactions = UserActivity.objects.filter(
        activity_type__in=['view', 'click', 'add_cart', 'purchase']
    ).values('user_id', 'product_id', 'activity_type')
    
    # Convert to DataFrame
    interactions_df = pd.DataFrame(list(interactions))
    
    if interactions_df.empty:
        logger.warning("No user interactions found")
        return pd.DataFrame(), pd.DataFrame()
    
    # Convert user_id to string (handles UUID and anonymous sessions)
    interactions_df['user_id'] = interactions_df['user_id'].astype(str)
    interactions_df['product_id'] = interactions_df['product_id'].astype(str)
    
    # Create interaction scores
    activity_weights = {
        'view': 1.0,
        'click': 2.0,
        'add_cart': 3.0,
        'purchase': 5.0,
    }
    
    interactions_df['interaction_score'] = interactions_df['activity_type'].map(activity_weights)
    
    # Aggregate interactions by user-product pair
    interactions_df = interactions_df.groupby(['user_id', 'product_id'], as_index=False).agg({
        'interaction_score': 'sum'
    })
    
    # Load product features
    products = Product.objects.filter(is_active=True).values(
        'id', 'price', 'average_rating', 'purchase_count', 'view_count'
    )
    
    products_df = pd.DataFrame(list(products))
    
    if products_df.empty:
        logger.warning("No products found")
        return interactions_df, pd.DataFrame()
    
    # Convert product id to string
    products_df['id'] = products_df['id'].astype(str)
    
    # Fill missing values
    products_df['price'] = products_df['price'].fillna(0)
    products_df['average_rating'] = products_df['average_rating'].fillna(0)
    products_df['purchase_count'] = products_df['purchase_count'].fillna(0)
    products_df['view_count'] = products_df['view_count'].fillna(0)
    
    logger.info(f"Loaded {len(interactions_df)} interactions and {len(products_df)} products")
    
    return interactions_df, products_df


def get_user_interaction_history(user_id, limit=50):
    """
    Get recent interaction history for a user
    
    Args:
        user_id: User ID
        limit: Maximum number of interactions to return
        
    Returns:
        DataFrame of user interactions
    """
    interactions = UserActivity.objects.filter(
        user_id=user_id
    ).order_by('-created_at')[:limit].values(
        'product_id', 'activity_type', 'created_at'
    )
    
    df = pd.DataFrame(list(interactions))
    
    if not df.empty:
        df['product_id'] = df['product_id'].astype(str)
    
    return df