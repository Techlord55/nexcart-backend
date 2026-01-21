# Location: apps\products\services.py
"""
NexCart Product Services
Business logic for product management
"""
from django.db.models import Avg, F
from django.core.cache import cache
from .models import Product, ProductReview
import logging

logger = logging.getLogger(__name__)


class ProductService:
    """Product business logic"""
    
    @staticmethod
    def update_product_rating(product_id):
        """Update product average rating and review count"""
        try:
            product = Product.objects.get(id=product_id)
            reviews = ProductReview.objects.filter(
                product=product,
                is_approved=True
            )
            
            aggregate = reviews.aggregate(
                avg_rating=Avg('rating'),
                count=F('id')
            )
            
            product.average_rating = aggregate['avg_rating'] or 0
            product.review_count = reviews.count()
            product.save(update_fields=['average_rating', 'review_count'])
            
            # Clear cache
            cache_key = f'product_detail_{product_id}'
            cache.delete(cache_key)
            
            logger.info(f"Updated rating for product {product_id}")
            
        except Product.DoesNotExist:
            logger.error(f"Product {product_id} not found")
    
    @staticmethod
    def increment_view_count(product_id):
        """Increment product view count"""
        try:
            Product.objects.filter(id=product_id).update(
                view_count=F('view_count') + 1
            )
        except Exception as e:
            logger.error(f"Error incrementing view count: {str(e)}")
    
    @staticmethod
    def increment_purchase_count(product_id, quantity=1):
        """Increment product purchase count"""
        try:
            Product.objects.filter(id=product_id).update(
                purchase_count=F('purchase_count') + quantity
            )
        except Exception as e:
            logger.error(f"Error incrementing purchase count: {str(e)}")
    
    @staticmethod
    def check_stock_availability(product_id, quantity):
        """Check if product has enough stock"""
        try:
            product = Product.objects.get(id=product_id)
            
            if not product.track_inventory:
                return True
            
            if product.stock_quantity >= quantity:
                return True
            
            if product.allow_backorder:
                return True
            
            return False
            
        except Product.DoesNotExist:
            return False
    
    @staticmethod
    def reduce_stock(product_id, quantity):
        """Reduce product stock quantity"""
        try:
            product = Product.objects.get(id=product_id)
            
            if product.track_inventory:
                if product.stock_quantity >= quantity:
                    product.stock_quantity -= quantity
                    product.save(update_fields=['stock_quantity'])
                    logger.info(f"Reduced stock for product {product_id} by {quantity}")
                else:
                    logger.warning(f"Insufficient stock for product {product_id}")
            
        except Product.DoesNotExist:
            logger.error(f"Product {product_id} not found")
    
    @staticmethod
    def restore_stock(product_id, quantity):
        """Restore product stock quantity (e.g., after order cancellation)"""
        try:
            product = Product.objects.get(id=product_id)
            
            if product.track_inventory:
                product.stock_quantity += quantity
                product.save(update_fields=['stock_quantity'])
                logger.info(f"Restored stock for product {product_id} by {quantity}")
            
        except Product.DoesNotExist:
            logger.error(f"Product {product_id} not found")