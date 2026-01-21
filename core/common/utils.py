# Location: core\common\utils.py
"""
NexCart Common Utilities
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler for DRF"""
    
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Log the exception
    logger.error(f"Exception: {exc}, Context: {context}")
    
    if response is not None:
        # Customize the response data
        custom_response_data = {
            'error': True,
            'message': str(exc),
            'details': response.data
        }
        response.data = custom_response_data
    
    return response


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_unique_code(prefix='', length=8):
    """Generate unique code"""
    import uuid
    code = str(uuid.uuid4()).replace('-', '').upper()[:length]
    return f"{prefix}{code}" if prefix else code