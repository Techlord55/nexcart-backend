# Location: core\common\permissions.py
"""
NexCart Custom Permissions
"""
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Allow access only to admin users"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow access to object owner or admin"""
    
    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if request.user.role == 'admin':
            return True
        
        # Check if object has user field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class ReadOnly(permissions.BasePermission):
    """Allow read-only access"""
    
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS