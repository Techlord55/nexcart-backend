# Location: apps\users\tests.py
"""
NexCart User Tests
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, UserProfile


class UserModelTest(TestCase):
    """Test user model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertEqual(self.user.full_name, 'Test User')
    
    def test_user_profile_created(self):
        """Test user profile is created with user"""
        profile = UserProfile.objects.create(user=self.user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.user)


class AuthenticationAPITest(APITestCase):
    """Test authentication endpoints"""
    
    def test_user_registration(self):
        """Test user can register"""
        url = reverse('users:register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)
    
    def test_user_login(self):
        """Test user can login"""
        # Create user
        user = User.objects.create_user(
            email='logintest@example.com',
            password='testpass123'
        )
        
        url = reverse('users:login')
        data = {
            'email': 'logintest@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        url = reverse('users:login')
        data = {
            'email': 'invalid@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)