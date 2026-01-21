"""
NexCart Payments URLs
"""
from django.urls import path
from .views import initiate_payment, check_payment_status
from .webhooks import mesomb_webhook

app_name = 'payments'

urlpatterns = [
    # Payment operations
    path('payments/initiate/', initiate_payment, name='payment-initiate'),
    path('payments/status/<str:transaction_id>/', check_payment_status, name='payment-status'),
    
    # Webhooks
    path('webhooks/mesomb/', mesomb_webhook, name='mesomb-webhook'),
]