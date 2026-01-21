# Location: apps\payments\webhooks.py
"""
NexCart Payment Webhooks
Handle payment gateway callbacks
"""
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import logging

from .services import MeSombPaymentService, PaymentException

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def mesomb_webhook(request):
    """Handle MeSomb payment webhooks"""
    try:
        # Get signature from headers
        signature = request.META.get('HTTP_X_MESOMB_SIGNATURE', '')
        
        # Parse request body
        payload = json.loads(request.body.decode('utf-8'))
        
        logger.info(f"Received MeSomb webhook: {payload}")
        
        # Process webhook
        payment_service = MeSombPaymentService()
        result = payment_service.process_webhook(payload, signature)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Webhook processed',
            'data': result
        }, status=200)
        
    except PaymentException as e:
        logger.error(f"Webhook processing failed: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected webhook error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Webhook processing failed'
        }, status=500)