"""
NexCart Orders URLs
"""
from django.urls import path
from .views import (
    CartView,
    add_to_cart,
    update_cart_item,
    remove_from_cart,
    clear_cart,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    cart_item_operations
)

app_name = 'orders'

urlpatterns = [
    # Cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', add_to_cart, name='cart-add'),
    path('cart/items/<uuid:item_id>/', cart_item_operations, name='cart-item-operations'),
    path('cart/clear/', clear_cart, name='cart-clear'),
    
    # Orders
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<uuid:id>/', OrderDetailView.as_view(), name='order-detail'),
]
