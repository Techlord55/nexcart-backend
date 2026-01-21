from django.contrib import admin
from django.utils.html import format_html
from .models import Payment, Refund


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'order', 'amount', 'payment_method', 'status_badge', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['transaction_id', 'order__id']
    readonly_fields = ['order', 'amount', 'payment_method', 'transaction_id', 'currency', 'raw_response', 'created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('order', 'transaction_id', 'amount', 'currency', 'payment_method')
        }),
        ('Status', {
            'fields': ('status', 'completed_at')
        }),
        ('Raw Data', {
            'fields': ('raw_response',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'completed': '#28A745',
            'failed': '#DC3545',
            'refunded': '#6C757D',
        }
        color = colors.get(obj.status, '#6C757D')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['refund_id', 'payment', 'amount', 'status_badge', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['refund_id', 'payment__transaction_id']
    readonly_fields = ['payment', 'refund_id', 'amount', 'reason', 'raw_response', 'created_at', 'completed_at']
    
    fieldsets = (
        ('Refund Information', {
            'fields': ('payment', 'refund_id', 'amount', 'reason')
        }),
        ('Status', {
            'fields': ('status', 'completed_at')
        }),
        ('Raw Data', {
            'fields': ('raw_response',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'completed': '#28A745',
            'failed': '#DC3545',
        }
        color = colors.get(obj.status, '#6C757D')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
