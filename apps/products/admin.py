from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductReview, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    ordering = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'image_preview', 'alt_text', 'position']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px; object-fit: contain;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_thumbnail', 'category', 'price', 'stock_quantity', 'is_active', 'is_featured', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_featured', 'stock_quantity', 'price']
    readonly_fields = ['main_image_preview', 'created_at', 'updated_at', 'view_count', 'purchase_count', 'average_rating', 'review_count']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description', 'tags')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_price', 'cost_price')
        }),
        ('Inventory', {
            'fields': ('sku', 'stock_quantity', 'track_inventory', 'allow_backorder')
        }),
        ('Main Image', {
            'fields': ('featured_image', 'main_image_preview')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('view_count', 'purchase_count', 'average_rating', 'review_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.featured_image.url
            )
        return "No image"
    image_thumbnail.short_description = 'Image'
    
    def main_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 300px; object-fit: contain;" />',
                obj.featured_image.url
            )
        return "No image uploaded"
    main_image_preview.short_description = 'Current Main Image'
    
    class Media:
        css = {
            'all': ['admin/css/custom_admin.css']
        }


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_thumbnail', 'alt_text', 'position']
    list_filter = ['product__category']
    search_fields = ['product__name', 'alt_text']
    list_editable = ['position']
    readonly_fields = ['image_preview']
    
    fields = ['product', 'image', 'image_preview', 'alt_text', 'position']
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No image"
    image_thumbnail.short_description = 'Thumbnail'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 400px; max-width: 400px; object-fit: contain;" />',
                obj.image.url
            )
        return "No image uploaded"
    image_preview.short_description = 'Full Preview'


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_verified_purchase', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_verified_purchase', 'is_approved', 'created_at']
    search_fields = ['product__name', 'user__email', 'comment']
    list_editable = ['is_approved']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'user', 'rating', 'title', 'comment')
        }),
        ('Status', {
            'fields': ('is_verified_purchase', 'is_approved', 'helpful_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'product__name']
    readonly_fields = ['created_at']
