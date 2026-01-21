# Location: core/middleware/session_middleware.py
"""
Custom Session Middleware for handling CORS sessions
"""
import logging

logger = logging.getLogger(__name__)


class SessionDebugMiddleware:
    """Middleware to debug and ensure session persistence"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Log session info before request
        session_key_before = request.session.session_key
        logger.info(f"Request: {request.method} {request.path} | Session Before: {session_key_before}")
        
        # Ensure session exists
        if not request.session.session_key:
            request.session.create()
            logger.info(f"Created new session: {request.session.session_key}")
        
        # Force session to be saved
        request.session.modified = True
        
        response = self.get_response(request)
        
        # Log session info after request
        session_key_after = request.session.session_key
        logger.info(f"Response: {response.status_code} | Session After: {session_key_after}")
        
        return response
