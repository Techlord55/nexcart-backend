from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, Cart, CartItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'quantity', 'price', 'subtotal']
    can_delete = False
    fields = ['product_name', 'quantity', 'price', 'subtotal']
    
    def subtotal(self, obj):
        return f"${obj.total:.2f}"
    subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status_badge', 'payment_status_badge', 'total', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__email', 'user__first_name', 'user__last_name', 'email']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'shipped_at', 'delivered_at', 'total_display']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'total_display', 'created_at', 'updated_at')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Shipping Address', {
            'fields': (
                'shipping_first_name', 'shipping_last_name',
                'shipping_address_line1', 'shipping_address_line2',
                'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country'
            )
        }),
        ('Billing Address', {
            'fields': (
                'billing_same_as_shipping',
                'billing_first_name', 'billing_last_name',
                'billing_address_line1', 'billing_address_line2',
                'billing_city', 'billing_state', 'billing_postal_code', 'billing_country'
            ),
            'classes': ('collapse',)
        }),
        ('Pricing', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total')
        }),
        ('Shipping Details', {
            'fields': ('tracking_number', 'carrier', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'processing': '#007BFF',
            'shipped': '#17A2B8',
            'delivered': '#28A745',
            'cancelled': '#DC3545',
            'refunded': '#6C757D',
        }
        color = colors.get(obj.status, '#6C757D')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def payment_status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'completed': '#28A745',
            'failed': '#DC3545',
            'refunded': '#6C757D',
        }
        color = colors.get(obj.payment_status, '#6C757D')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment'
    
    def total_display(self, obj):
        return f"${obj.total:.2f}"
    total_display.short_description = 'Total Amount'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'price', 'item_total']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['order__order_number', 'product_name', 'product_sku']
    readonly_fields = ['order', 'product', 'product_name', 'quantity', 'price', 'total']
    
    def item_total(self, obj):
        return f"${obj.total:.2f}"
    item_total.short_description = 'Total'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'item_total']
    fields = ['product', 'quantity', 'price', 'item_total']
    
    def item_total(self, obj):
        return f"${obj.total_price:.2f}"
    item_total.short_description = 'Total'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_display', 'total_items_display', 'subtotal_display', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'session_id']
    readonly_fields = ['created_at', 'updated_at', 'total_items_display', 'subtotal_display']
    inlines = [CartItemInline]
    
    fieldsets = (
        ('Cart Information', {
            'fields': ('user', 'session_id', 'total_items_display', 'subtotal_display')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_display(self, obj):
        return obj.user.email if obj.user else f"Guest ({obj.session_id[:8]})"
    user_display.short_description = 'User'
    
    def total_items_display(self, obj):
        return obj.total_items
    total_items_display.short_description = 'Total Items'
    
    def subtotal_display(self, obj):
        return f"${obj.subtotal:.2f}"
    subtotal_display.short_description = 'Subtotal'


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_number', 'notes']
    readonly_fields = ['order', 'status', 'created_by', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
