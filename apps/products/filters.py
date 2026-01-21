# Location: apps\products\filters.py
"""
NexCart Product Filters
"""
import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    """Product filter for search and filtering"""
    
    name = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.UUIDFilter(field_name='category__id')
    is_featured = django_filters.BooleanFilter()
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Product
        fields = ['name', 'category', 'is_featured', 'min_price', 'max_price']
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock_quantity__gt=0) | queryset.filter(allow_backorder=True)
        return queryset
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            name__icontains=value
        ) | queryset.filter(
            description__icontains=value
        ) | queryset.filter(
            tags__icontains=value
        )