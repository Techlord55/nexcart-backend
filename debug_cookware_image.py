"""
Debug why some products show "No Image" on frontend despite having images in DB
"""
from dotenv import load_dotenv
from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

import django
import sys
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings.dev')
django.setup()

from apps.products.models import Product
from apps.products.serializers import ProductListSerializer
from django.test import RequestFactory

print("=" * 80)
print("DEBUG: Non-Stick Cookware Set Image Issue")
print("=" * 80)

# Get the problematic product
product = Product.objects.filter(name="Non-Stick Cookware Set").first()

if not product:
    print("Product not found!")
    sys.exit(1)

print(f"\nProduct: {product.name}")
print(f"ID: {product.id}")

# Check database field
print(f"\n📁 Database Field:")
print(f"   featured_image.name: {product.featured_image.name if product.featured_image else 'None'}")
if product.featured_image:
    try:
        print(f"   featured_image.url: {product.featured_image.url}")
    except Exception as e:
        print(f"   Error getting URL: {e}")

# Check API serialization
factory = RequestFactory()
request = factory.get('/')
request.META['HTTP_HOST'] = 'localhost:8000'
request.META['wsgi.url_scheme'] = 'http'

serializer = ProductListSerializer(product, context={'request': request})
data = serializer.data

print(f"\n📡 API Response:")
print(json.dumps(data, indent=2, default=str))

# Check if URL is valid
if data.get('featured_image'):
    print(f"\n🔍 Testing Image URL:")
    print(f"   URL: {data['featured_image']}")
    
    import requests
    try:
        response = requests.head(data['featured_image'], timeout=5)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Image is accessible")
        else:
            print(f"   ❌ Image returned error code")
    except Exception as e:
        print(f"   ❌ Cannot access image: {e}")
else:
    print(f"\n❌ No featured_image in API response!")

print("\n" + "=" * 80)
