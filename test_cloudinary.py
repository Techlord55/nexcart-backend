#!/usr/bin/env python
"""
Test Cloudinary Configuration
Run this to verify Cloudinary is properly configured
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings.dev')

# Setup Django
import django
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
import cloudinary

print("=" * 60)
print("CLOUDINARY CONFIGURATION TEST")
print("=" * 60)

# Check environment variables
print("\n1. Environment Variables:")
print(f"   CLOUDINARY_CLOUD_NAME: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
print(f"   CLOUDINARY_API_KEY: {os.getenv('CLOUDINARY_API_KEY')}")
print(f"   CLOUDINARY_SECRET: {'*' * 10 if os.getenv('CLOUDINARY_SECRET') else 'NOT SET'}")

# Check Django settings
print("\n2. Django Settings:")
print(f"   CLOUDINARY_STORAGE: {settings.CLOUDINARY_STORAGE}")
print(f"   DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")

# Check cloudinary config
print("\n3. Cloudinary Config:")
print(f"   cloud_name: {cloudinary.config().cloud_name}")
print(f"   api_key: {cloudinary.config().api_key}")
print(f"   api_secret: {'*' * 10 if cloudinary.config().api_secret else 'NOT SET'}")

# Check default storage backend
print("\n4. Storage Backend:")
print(f"   Type: {type(default_storage)}")
print(f"   Class: {default_storage.__class__.__name__}")

# Test if it's actually using Cloudinary
if 'cloudinary' in default_storage.__class__.__module__.lower():
    print("   ✅ Using Cloudinary Storage!")
else:
    print("   ❌ NOT using Cloudinary Storage!")
    print(f"   Current backend: {default_storage.__class__.__module__}")

print("\n" + "=" * 60)

# Try a simple upload test
try:
    print("\n5. Upload Test:")
    from django.core.files.base import ContentFile
    
    # Create a dummy file
    test_file = ContentFile(b"Test content", name="test.txt")
    
    # Try to save it
    file_path = default_storage.save('test/cloudinary_test.txt', test_file)
    print(f"   File saved to: {file_path}")
    
    # Get the URL
    file_url = default_storage.url(file_path)
    print(f"   File URL: {file_url}")
    
    if 'cloudinary.com' in file_url:
        print("   ✅ Upload successful - File is on Cloudinary!")
        # Clean up
        default_storage.delete(file_path)
        print("   ✅ Cleanup successful")
    else:
        print(f"   ❌ Upload failed - File is NOT on Cloudinary!")
        print(f"   URL should contain 'cloudinary.com'")
        
except Exception as e:
    print(f"   ❌ Error during upload test: {e}")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)
