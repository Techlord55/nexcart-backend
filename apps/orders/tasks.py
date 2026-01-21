# Location: apps\orders\tasks.py
"""
NexCart Order Celery Tasks
Background tasks for order processing
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, OrderStatusHistory
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_order(order_id):
    """Process order after payment confirmation"""
    try:
        order = Order.objects.get(id=order_id)
        
        # Send order confirmation email
        send_order_confirmation_email.delay(str(order.id))
        
        # Update order status
        order.status = 'processing'
        order.save()
        
        # Create status history
        OrderStatusHistory.objects.create(
            order=order,
            status='processing',
            notes='Payment confirmed, order is being processed'
        )
        
        logger.info(f"Order {order.order_number} processed successfully")
        
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")
    except Exception as e:
        logger.error(f"Error processing order {order_id}: {str(e)}")


@shared_task
def send_order_confirmation_email(order_id):
    """Send order confirmation email to customer"""
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Order Confirmation - {order.order_number}'
        message = f"""
        Dear {order.shipping_first_name},
        
        Thank you for your order!
        
        Order Number: {order.order_number}
        Total Amount: ${order.total}
        
        We'll send you another email when your order ships.
        
        Best regards,
        NexCart Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=False,
        )
        
        logger.info(f"Order confirmation email sent for {order.order_number}")
        
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")
    except Exception as e:
        logger.error(f"Error sending confirmation email: {str(e)}")


@shared_task
def send_shipping_notification(order_id):
    """Send shipping notification email"""
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Your Order Has Shipped - {order.order_number}'
        message = f"""
        Dear {order.shipping_first_name},
        
        Great news! Your order has been shipped.
        
        Order Number: {order.order_number}
        Tracking Number: {order.tracking_number}
        Carrier: {order.carrier}
        
        You can track your package using the tracking number above.
        
        Best regards,
        NexCart Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=False,
        )
        
        logger.info(f"Shipping notification sent for {order.order_number}")
        
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")
    except Exception as e:
        logger.error(f"Error sending shipping notification: {str(e)}")


@shared_task
def cancel_expired_orders():
    """Cancel orders that have been pending for too long"""
    from django.utils import timezone
    from datetime import timedelta
    
    try:
        # Cancel orders pending for more than 24 hours
        expiry_time = timezone.now() - timedelta(hours=24)
        
        expired_orders = Order.objects.filter(
            status='pending',
            payment_status='pending',
            created_at__lt=expiry_time
        )
        
        for order in expired_orders:
            order.status = 'cancelled'
            order.save()
            
            # Restore stock
            from apps.products.services import ProductService
            for item in order.items.all():
                ProductService.restore_stock(item.product.id, item.quantity)
            
            # Create status history
            OrderStatusHistory.objects.create(
                order=order,
                status='cancelled',
                notes='Order cancelled due to payment timeout'
            )
            
            logger.info(f"Order {order.order_number} cancelled due to expiry")
        
        logger.info(f"Cancelled {expired_orders.count()} expired orders")
        
    except Exception as e:
        logger.error(f"Error cancelling expired orders: {str(e)}")