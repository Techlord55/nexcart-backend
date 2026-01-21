# Location: apps\users\views.py
"""
NexCart Authentication Views
Email/password and OAuth2 social authentication
"""
from rest_framework import status, generics,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings
import requests
import logging

from .models import User, UserProfile, StoreSettings
from .permissions import IsAdmin
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    StoreSettingsSerializer
)

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    """User registration with email/password"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """User login with email/password"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, email=email, password=password)
            
            if user:
                if not user.is_active:
                    return Response({
                        'error': 'Account is disabled'
                    }, status=status.HTTP_403_FORBIDDEN)
                
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                
                # Update last login
                user.save(update_fields=['last_login'])
                
                return Response({
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })
            
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthView(APIView):
    """Google OAuth2 authentication"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response({
                'error': 'Token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Verify Google token
            google_response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if google_response.status_code != 200:
                return Response({
                    'error': 'Invalid Google token'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user_info = google_response.json()
            email = user_info.get('email')
            provider_id = user_info.get('sub')
            
            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': user_info.get('given_name', ''),
                    'last_name': user_info.get('family_name', ''),
                    'auth_provider': 'google',
                    'provider_id': provider_id,
                    'is_verified': True,
                }
            )
            
            if created:
                # Create profile
                UserProfile.objects.create(user=user)
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'created': created
            })
            
        except Exception as e:
            logger.error(f"Google auth error: {str(e)}")
            return Response({
                'error': 'Authentication failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DiscordAuthView(APIView):
    """Discord OAuth2 authentication"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        code = request.data.get('code')
        redirect_uri = request.data.get('redirect_uri')
        
        if not code:
            return Response({
                'error': 'Code is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Exchange code for access token
            token_response = requests.post(
                'https://discord.com/api/oauth2/token',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                data={
                    'client_id': settings.DISCORD_CLIENT_ID,
                    'client_secret': settings.DISCORD_CLIENT_SECRET,
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': redirect_uri,
                }
            )
            
            token_data = token_response.json()
            access_token = token_data.get('access_token')
            
            if not access_token:
                return Response({
                    'error': 'Failed to get access token'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get user info
            user_response = requests.get(
                'https://discord.com/api/users/@me',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            
            user_info = user_response.json()
            email = user_info.get('email')
            
            if not email:
                return Response({
                    'error': 'Email not available from Discord'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Parse username for first/last name
            username = user_info.get('username', '')
            global_name = user_info.get('global_name', username)
            name_parts = global_name.split()
            
            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': name_parts[0] if name_parts else username,
                    'last_name': ' '.join(name_parts[1:]) if len(name_parts) > 1 else '',
                    'auth_provider': 'discord',
                    'provider_id': user_info.get('id'),
                    'is_verified': user_info.get('verified', True),
                }
            )
            
            if created:
                UserProfile.objects.create(user=user)
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'created': created
            })
            
        except Exception as e:
            logger.error(f"Discord auth error: {str(e)}")
            return Response({
                'error': 'Authentication failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MicrosoftAuthView(APIView):
    """Microsoft OAuth2 authentication"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        code = request.data.get('code')
        
        if not code:
            return Response({
                'error': 'Code is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Exchange code for access token
            token_response = requests.post(
                'https://login.microsoftonline.com/common/oauth2/v2.0/token',
                data={
                    'client_id': settings.MICROSOFT_CLIENT_ID,
                    'client_secret': settings.MICROSOFT_CLIENT_SECRET,
                    'code': code,
                    'redirect_uri': request.data.get('redirect_uri'),
                    'grant_type': 'authorization_code',
                }
            )
            
            token_data = token_response.json()
            access_token = token_data.get('access_token')
            
            if not access_token:
                return Response({
                    'error': 'Failed to get access token'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get user info
            user_response = requests.get(
                'https://graph.microsoft.com/v1.0/me',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            
            user_info = user_response.json()
            email = user_info.get('mail') or user_info.get('userPrincipalName')
            
            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': user_info.get('givenName', ''),
                    'last_name': user_info.get('surname', ''),
                    'auth_provider': 'microsoft',
                    'provider_id': user_info.get('id'),
                    'is_verified': True,
                }
            )
            
            if created:
                UserProfile.objects.create(user=user)
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'created': created
            })
            
        except Exception as e:
            logger.error(f"Microsoft auth error: {str(e)}")
            return Response({
                'error': 'Authentication failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """Change user password"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'error': 'Wrong password'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({'message': 'Password updated successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# Add this class at the bottom of views.py
class UserListView(generics.ListAPIView):
    """Admin-only view to list all users"""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

# Add to apps/users/views.py

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin-only view to update or delete any user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        # Prevent admin from deleting themselves
        if instance == self.request.user:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"error": "You cannot delete your own account"})
        instance.delete()
    
    def perform_update(self, serializer):
        # When role is changed to admin, set is_staff=True
        if 'role' in self.request.data:
            if self.request.data['role'] == 'admin':
                serializer.save(is_staff=True, is_superuser=True)
            else:
                serializer.save(is_staff=False, is_superuser=False)
        else:
            serializer.save()

class StoreSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = StoreSettingsSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        return StoreSettings.load()
