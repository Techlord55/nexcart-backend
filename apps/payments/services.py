# Location: apps\payments\services.py
"""
NexCart Payment Service
MeSomb payment integration for mobile money payments
"""
import hashlib
import hmac
import json
import requests
import logging
from decimal import Decimal
from typing import Dict, Optional
from django.conf import settings
from django.utils import timezone

from apps.orders.models import Order

logger = logging.getLogger(__name__)


class MeSombPaymentService:
    """
    MeSomb Payment Gateway Integration
    Supports MTN Mobile Money, Orange Money, etc.
    """
    
    BASE_URL = "https://mesomb.hachther.com/api/v1.1"
    
    def __init__(self):
        self.app_key = settings.MESOMB_APP_KEY
        self.access_key = settings.MESOMB_ACCESS_KEY
        self.secret_key = settings.MESOMB_SECRET_KEY
    
    def _generate_signature(self, data: str) -> str:
        """Generate HMAC signature for request authentication"""
        return hmac.new(
            self.secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _make_request(
        self,
        endpoint: str,
        method: str = 'POST',
        data: Optional[Dict] = None
    ) -> Dict:
        """Make authenticated request to MeSomb API"""
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        headers = {
            'X-MeSomb-Application': self.app_key,
            'X-MeSomb-AccessKey': self.access_key,
            'Content-Type': 'application/json',
        }
        
        if data:
            json_data = json.dumps(data)
            headers['X-MeSomb-Signature'] = self._generate_signature(json_data)
        else:
            json_data = None
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=json_data,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"MeSomb API error: {str(e)}")
            raise PaymentException(f"Payment service error: {str(e)}")
    
    def initiate_payment(
        self,
        order: Order,
        phone_number: str,
        service: str = 'MTN',
        currency: str = 'XAF'
    ) -> Dict:
        """
        Initiate a mobile money payment
        
        Args:
            order: Order instance
            phone_number: Customer phone number (format: 237XXXXXXXXX)
            service: Payment service (MTN, ORANGE, etc.)
            currency: Currency code (XAF for Central Africa)
            
        Returns:
            Payment response data
        """
        
        amount = float(order.total)
        
        payload = {
            'amount': amount,
            'service': service,
            'payer': phone_number,
            'currency': currency,
            'reference': order.order_number,
            'trxID': str(order.id),
            'redirect_url': f"{settings.FRONTEND_URL}/orders/{order.id}/payment-success",
            'extra': {
                'order_id': str(order.id),
                'customer_email': order.email,
            }
        }
        
        try:
            response = self._make_request('payment/collect', data=payload)
            
            logger.info(f"Payment initiated for order {order.order_number}: {response}")
            
            # Create payment record
            from .models import Payment
            Payment.objects.create(
                order=order,
                transaction_id=response.get('transaction_id') or response.get('pk'),
                payment_method=service,
                amount=order.total,
                currency=currency,
                status='pending',
                raw_response=response
            )
            
            return {
                'success': True,
                'transaction_id': response.get('transaction_id'),
                'status': response.get('status'),
                'message': 'Payment initiated successfully'
            }
            
        except Exception as e:
            logger.error(f"Payment initiation failed: {str(e)}")
            raise PaymentException(str(e))
    
    def check_payment_status(self, transaction_id: str) -> Dict:
        """
        Check payment transaction status
        
        Args:
            transaction_id: MeSomb transaction ID
            
        Returns:
            Payment status data
        """
        
        try:
            response = self._make_request(
                f'payment/status/{transaction_id}',
                method='GET'
            )
            
            return {
                'transaction_id': transaction_id,
                'status': response.get('status'),
                'amount': response.get('amount'),
                'currency': response.get('currency'),
                'data': response
            }
            
        except Exception as e:
            logger.error(f"Status check failed: {str(e)}")
            raise PaymentException(str(e))
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """
        Verify webhook signature from MeSomb
        
        Args:
            payload: Raw webhook payload
            signature: Signature from X-MeSomb-Signature header
            
        Returns:
            True if signature is valid
        """
        
        expected_signature = self._generate_signature(payload)
        return hmac.compare_digest(expected_signature, signature)
    
    def process_webhook(self, payload: Dict, signature: str) -> Dict:
        """
        Process payment webhook from MeSomb
        
        Args:
            payload: Webhook payload
            signature: Request signature
            
        Returns:
            Processing result
        """
        
        # Verify signature
        if not self.verify_webhook_signature(json.dumps(payload), signature):
            raise PaymentException("Invalid webhook signature")
        
        from .models import Payment
        
        transaction_id = payload.get('transaction_id')
        status = payload.get('status')
        order_id = payload.get('extra', {}).get('order_id')
        
        if not all([transaction_id, status, order_id]):
            raise PaymentException("Invalid webhook data")
        
        try:
            # Update payment record
            payment = Payment.objects.get(transaction_id=transaction_id)
            payment.status = self._map_mesomb_status(status)
            payment.raw_response = payload
            payment.save()
            
            # Update order
            order = Order.objects.get(id=order_id)
            
            if payment.status == 'completed':
                order.payment_status = 'completed'
                order.status = 'processing'
                
                # Trigger order processing
                from apps.orders.tasks import process_order
                process_order.delay(str(order.id))
            
            elif payment.status == 'failed':
                order.payment_status = 'failed'
            
            order.save()
            
            logger.info(f"Webhook processed for order {order.order_number}")
            
            return {
                'success': True,
                'order_id': str(order.id),
                'payment_status': payment.status
            }
            
        except Exception as e:
            logger.error(f"Webhook processing error: {str(e)}")
            raise PaymentException(str(e))
    
    def _map_mesomb_status(self, mesomb_status: str) -> str:
        """Map MeSomb status to internal payment status"""
        
        status_mapping = {
            'SUCCESS': 'completed',
            'PENDING': 'pending',
            'FAILED': 'failed',
            'EXPIRED': 'failed',
        }
        
        return status_mapping.get(mesomb_status.upper(), 'pending')
    
    def refund_payment(self, transaction_id: str, amount: Optional[Decimal] = None) -> Dict:
        """
        Refund a payment
        
        Args:
            transaction_id: Original transaction ID
            amount: Amount to refund (None for full refund)
            
        Returns:
            Refund response data
        """
        
        payload = {
            'transaction_id': transaction_id,
        }
        
        if amount:
            payload['amount'] = float(amount)
        
        try:
            response = self._make_request('payment/refund', data=payload)
            
            logger.info(f"Refund processed for transaction {transaction_id}")
            
            return {
                'success': True,
                'refund_id': response.get('refund_id'),
                'status': response.get('status'),
                'message': 'Refund processed successfully'
            }
            
        except Exception as e:
            logger.error(f"Refund failed: {str(e)}")
            raise PaymentException(str(e))


class PaymentException(Exception):
    """Custom exception for payment errors"""
    pass