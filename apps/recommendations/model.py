# Location: apps\recommendations\model.py
"""
NexCart AI Recommendation Engine
Hybrid recommendation system combining collaborative and content-based filtering
"""
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix
import pickle
import logging
from pathlib import Path
from typing import List, Dict, Tuple
from django.conf import settings

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Hybrid recommendation system using:
    1. Collaborative Filtering (User-based and Item-based)
    2. Content-Based Filtering
    3. Popularity-based fallback
    """
    
    def __init__(self):
        self.user_item_matrix = None
        self.product_features = None
        self.similarity_matrix = None
        self.svd_model = None
        self.scaler = StandardScaler()
        self.product_id_mapping = {}
        self.reverse_product_mapping = {}
        self.user_id_mapping = {}
        self.reverse_user_mapping = {}
        
    def prepare_data(self, interactions_df: pd.DataFrame, products_df: pd.DataFrame):
        """
        Prepare data for recommendation models
        
        Args:
            interactions_df: DataFrame with columns [user_id, product_id, interaction_score]
            products_df: DataFrame with product features
        """
        logger.info("Preparing recommendation data...")
        
        # Create user and product mappings
        unique_users = interactions_df['user_id'].unique()
        unique_products = interactions_df['product_id'].unique()
        
        self.user_id_mapping = {uid: idx for idx, uid in enumerate(unique_users)}
        self.reverse_user_mapping = {idx: uid for uid, idx in self.user_id_mapping.items()}
        
        self.product_id_mapping = {pid: idx for idx, pid in enumerate(unique_products)}
        self.reverse_product_mapping = {idx: pid for pid, idx in self.product_id_mapping.items()}
        
        # Build user-item interaction matrix
        self._build_user_item_matrix(interactions_df)
        
        # Build product feature matrix
        self._build_product_features(products_df)
        
        logger.info(f"Data prepared: {len(unique_users)} users, {len(unique_products)} products")
    
    def _build_user_item_matrix(self, interactions_df: pd.DataFrame):
        """Build sparse user-item interaction matrix"""
        
        # Map IDs to indices
        interactions_df['user_idx'] = interactions_df['user_id'].map(self.user_id_mapping)
        interactions_df['product_idx'] = interactions_df['product_id'].map(self.product_id_mapping)
        
        # Create sparse matrix
        n_users = len(self.user_id_mapping)
        n_products = len(self.product_id_mapping)
        
        self.user_item_matrix = csr_matrix(
            (interactions_df['interaction_score'].values,
             (interactions_df['user_idx'].values, interactions_df['product_idx'].values)),
            shape=(n_users, n_products)
        )
        
        logger.info(f"User-item matrix shape: {self.user_item_matrix.shape}")
    
    def _build_product_features(self, products_df: pd.DataFrame):
        """Build product feature matrix for content-based filtering"""
        
        # Select relevant features
        feature_columns = ['price', 'average_rating', 'purchase_count', 'view_count']
        
        # Filter products that are in our mapping
        products_df = products_df[products_df['id'].isin(self.product_id_mapping.keys())].copy()
        products_df['product_idx'] = products_df['id'].map(self.product_id_mapping)
        products_df = products_df.sort_values('product_idx')
        
        # Extract and normalize features
        feature_matrix = products_df[feature_columns].fillna(0).values
        self.product_features = self.scaler.fit_transform(feature_matrix)
        
        logger.info(f"Product features shape: {self.product_features.shape}")
    
    def train_collaborative_filtering(self, n_components: int = 50):
        """
        Train collaborative filtering model using SVD
        
        Args:
            n_components: Number of latent factors
        """
        logger.info("Training collaborative filtering model...")
        
        # Apply SVD for dimensionality reduction
        self.svd_model = TruncatedSVD(n_components=min(n_components, 
                                                       min(self.user_item_matrix.shape) - 1))
        self.user_factors = self.svd_model.fit_transform(self.user_item_matrix)
        self.item_factors = self.svd_model.components_.T
        
        logger.info(f"SVD model trained with {n_components} components")
    
    def train_content_based(self):
        """Train content-based filtering using product features"""
        logger.info("Training content-based filtering...")
        
        # Compute item-item similarity matrix
        self.similarity_matrix = cosine_similarity(self.product_features)
        
        logger.info("Content-based model trained")
    
    def get_collaborative_recommendations(
        self, 
        user_id: str, 
        n_recommendations: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Get recommendations using collaborative filtering
        
        Args:
            user_id: User ID
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of (product_id, score) tuples
        """
        if user_id not in self.user_id_mapping:
            return []
        
        user_idx = self.user_id_mapping[user_id]
        
        # Predict scores for all items
        user_vector = self.user_factors[user_idx]
        predicted_scores = np.dot(user_vector, self.item_factors.T)
        
        # Get items user hasn't interacted with
        interacted_items = self.user_item_matrix[user_idx].nonzero()[1]
        predicted_scores[interacted_items] = -np.inf
        
        # Get top N recommendations
        top_indices = np.argsort(predicted_scores)[::-1][:n_recommendations]
        
        recommendations = [
            (self.reverse_product_mapping[idx], float(predicted_scores[idx]))
            for idx in top_indices
        ]
        
        return recommendations
    
    def get_content_based_recommendations(
        self,
        product_id: str,
        n_recommendations: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Get similar products using content-based filtering
        
        Args:
            product_id: Product ID to find similar items for
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of (product_id, similarity_score) tuples
        """
        if product_id not in self.product_id_mapping:
            return []
        
        product_idx = self.product_id_mapping[product_id]
        
        # Get similarity scores
        similarity_scores = self.similarity_matrix[product_idx]
        
        # Exclude the product itself
        similarity_scores[product_idx] = -np.inf
        
        # Get top N similar products
        top_indices = np.argsort(similarity_scores)[::-1][:n_recommendations]
        
        recommendations = [
            (self.reverse_product_mapping[idx], float(similarity_scores[idx]))
            for idx in top_indices
        ]
        
        return recommendations
    
    def get_hybrid_recommendations(
        self,
        user_id: str,
        n_recommendations: int = 10,
        collaborative_weight: float = 0.6,
        content_weight: float = 0.4
    ) -> List[str]:
        """
        Get hybrid recommendations combining collaborative and content-based
        
        Args:
            user_id: User ID
            n_recommendations: Number of recommendations to return
            collaborative_weight: Weight for collaborative filtering
            content_weight: Weight for content-based filtering
            
        Returns:
            List of product IDs
        """
        # Get collaborative recommendations
        collab_recs = self.get_collaborative_recommendations(user_id, n_recommendations * 2)
        
        if not collab_recs:
            # Fallback to popular products for new users
            return self.get_popular_products(n_recommendations)
        
        # Combine with content-based for top collaborative recommendations
        hybrid_scores = {}
        
        for product_id, collab_score in collab_recs:
            # Get content-based similar products
            content_recs = self.get_content_based_recommendations(product_id, 5)
            
            # Add collaborative score
            if product_id not in hybrid_scores:
                hybrid_scores[product_id] = 0
            hybrid_scores[product_id] += collab_score * collaborative_weight
            
            # Add content-based scores
            for similar_id, content_score in content_recs:
                if similar_id not in hybrid_scores:
                    hybrid_scores[similar_id] = 0
                hybrid_scores[similar_id] += content_score * content_weight
        
        # Sort by score and return top N
        sorted_products = sorted(
            hybrid_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n_recommendations]
        
        return [product_id for product_id, _ in sorted_products]
    
    def get_popular_products(self, n_recommendations: int = 10) -> List[str]:
        """
        Get popular products based on interaction counts
        
        Args:
            n_recommendations: Number of products to return
            
        Returns:
            List of product IDs
        """
        # Sum interactions for each product
        product_popularity = np.array(self.user_item_matrix.sum(axis=0)).flatten()
        
        # Get top N popular products
        top_indices = np.argsort(product_popularity)[::-1][:n_recommendations]
        
        return [self.reverse_product_mapping[idx] for idx in top_indices]
    
    def save_model(self, filepath: Path):
        """Save trained model to disk"""
        model_data = {
            'user_item_matrix': self.user_item_matrix,
            'product_features': self.product_features,
            'similarity_matrix': self.similarity_matrix,
            'svd_model': self.svd_model,
            'scaler': self.scaler,
            'user_factors': self.user_factors,
            'item_factors': self.item_factors,
            'product_id_mapping': self.product_id_mapping,
            'reverse_product_mapping': self.reverse_product_mapping,
            'user_id_mapping': self.user_id_mapping,
            'reverse_user_mapping': self.reverse_user_mapping,
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: Path):
        """Load trained model from disk"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.user_item_matrix = model_data['user_item_matrix']
        self.product_features = model_data['product_features']
        self.similarity_matrix = model_data['similarity_matrix']
        self.svd_model = model_data['svd_model']
        self.scaler = model_data['scaler']
        self.user_factors = model_data['user_factors']
        self.item_factors = model_data['item_factors']
        self.product_id_mapping = model_data['product_id_mapping']
        self.reverse_product_mapping = model_data['reverse_product_mapping']
        self.user_id_mapping = model_data['user_id_mapping']
        self.reverse_user_mapping = model_data['reverse_user_mapping']
        
        logger.info(f"Model loaded from {filepath}")