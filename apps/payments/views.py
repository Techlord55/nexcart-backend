# Location: apps\payments\views.py
"""
NexCart Payment Views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.orders.models import Order
from .services import MeSombPaymentService, PaymentException
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    """Initiate payment for an order"""
    try:
        order_id = request.data.get('order_id')
        phone_number = request.data.get('phone_number')
        service = request.data.get('service', 'MTN')
        
        # Validate inputs
        if not all([order_id, phone_number]):
            return Response({
                'error': 'order_id and phone_number are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get order
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Check if order is already paid
        if order.payment_status == 'completed':
            return Response({
                'error': 'Order is already paid'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Initiate payment
        payment_service = MeSombPaymentService()
        result = payment_service.initiate_payment(
            order=order,
            phone_number=phone_number,
            service=service
        )
        
        return Response(result, status=status.HTTP_200_OK)
        
    except PaymentException as e:
        logger.error(f"Payment initiation failed: {str(e)}")
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({
            'error': 'Payment initiation failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_payment_status(request, transaction_id):
    """Check payment status"""
    try:
        payment_service = MeSombPaymentService()
        result = payment_service.check_payment_status(transaction_id)
        
        return Response(result, status=status.HTTP_200_OK)
        
    except PaymentException as e:
        logger.error(f"Status check failed: {str(e)}")
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({
            'error': 'Status check failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)