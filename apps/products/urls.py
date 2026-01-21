"""
NexCart Products URLs
"""
from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailView,
    FeaturedProductsView,
    ProductReviewListCreateView,
    WishlistView,
    WishlistAddView,
    WishlistRemoveView,
    track_activity
)

app_name = 'products'

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    
    # Products - Featured MUST come before detail view
    path('products/featured/', FeaturedProductsView.as_view(), name='featured-products'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<uuid:id>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Reviews
    path('products/<uuid:product_id>/reviews/', ProductReviewListCreateView.as_view(), name='product-reviews'),
    path('reviews/', ProductReviewListCreateView.as_view(), name='review-create'),
    
    # Wishlist
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/', WishlistAddView.as_view(), name='wishlist-add'),
    path('wishlist/<uuid:id>/', WishlistRemoveView.as_view(), name='wishlist-remove'),
    
    # Activity tracking
    path('activity/track/', track_activity, name='track-activity'),
]
