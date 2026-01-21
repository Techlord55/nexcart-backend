# Location: apps/users/permissions.py
"""
Custom permission classes for NexCart
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users with admin role.
    This checks the 'role' field instead of is_staff/is_superuser.
    """
    
    def has_permission(self, request, view):
        # User must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # User must have admin role
        return request.user.role == 'admin'


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to all,
    but write access only to admins.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for authenticated admin users
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.role == 'admin'
