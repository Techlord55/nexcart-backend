"""
Check what the API is actually returning for product images
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
print("API RESPONSE CHECK")
print("=" * 80)

# Create mock request
factory = RequestFactory()
request = factory.get('/')
request.META['HTTP_HOST'] = 'localhost:8000'
request.META['wsgi.url_scheme'] = 'http'

# Get first 3 products
products = Product.objects.all()[:3]

for i, product in enumerate(products, 1):
    print(f"\n{i}. {product.name}")
    print(f"   Product ID: {product.id}")
    
    # Check raw field
    print(f"\n   🗄️  Database Field:")
    if product.featured_image:
        print(f"   - Name: {product.featured_image.name}")
        print(f"   - URL: {product.featured_image.url}")
    else:
        print(f"   - No image")
    
    # Check serialized output
    print(f"\n   📡 API Will Return:")
    serializer = ProductListSerializer(product, context={'request': request})
    data = serializer.data
    
    if data.get('featured_image'):
        print(f"   - featured_image: {data['featured_image']}")
        
        # Test if the URL is valid
        if data['featured_image'].startswith('http'):
            print(f"   - ✅ Valid HTTP URL")
            
            # Check if it's actually a Cloudinary URL serving another URL
            if 'unsplash.com' in data['featured_image'] or 'placeholder.com' in data['featured_image']:
                print(f"   - ⚠️  WARNING: This appears to be an external URL stored in the field")
                print(f"   - This won't work properly. You need to upload actual image files.")
    else:
        print(f"   - featured_image: null")
    
    print(f"\n   📋 Full Product Data:")
    print(f"   {json.dumps(data, indent=6, default=str)}")
    print("\n" + "-" * 80)

print("\n" + "=" * 80)
print("DIAGNOSIS")
print("=" * 80)

products_with_external_urls = 0
products_with_real_images = 0
products_without_images = 0

for product in Product.objects.all():
    if product.featured_image and product.featured_image.name:
        if 'http' in product.featured_image.name:
            products_with_external_urls += 1
        else:
            products_with_real_images += 1
    else:
        products_without_images += 1

print(f"\n📊 Image Status:")
print(f"   - Products with external URLs (Unsplash, etc.): {products_with_external_urls}")
print(f"   - Products with real uploaded images: {products_with_real_images}")
print(f"   - Products without images: {products_without_images}")

if products_with_external_urls > 0:
    print(f"\n⚠️  ISSUE FOUND!")
    print(f"   You have {products_with_external_urls} products with external URLs in the image field.")
    print(f"   These are not actual uploaded images - they're just URLs to external sites.")
    print(f"\n💡 SOLUTION:")
    print(f"   You need to upload actual image FILES, not URLs:")
    print(f"   1. Go to Django Admin: http://localhost:8000/admin/products/product/")
    print(f"   2. Edit a product")
    print(f"   3. In the 'Featured image' field, click 'Choose File' and upload a real image file")
    print(f"   4. Save the product")
    print(f"   5. The image will automatically be uploaded to Cloudinary")

print("\n" + "=" * 80)
