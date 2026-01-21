"""
NexCart Recommendations URLs
"""
from django.urls import path
from .services import (
    get_recommendations,
    get_similar_products,
    retrain_model
)

app_name = 'recommendations'

urlpatterns = [
    path('recommendations/', get_recommendations, name='recommendations'),
    path('recommendations/similar/<uuid:product_id>/', get_similar_products, name='similar-products'),
    path('recommendations/retrain/', retrain_model, name='retrain-model'),
]