"""
Quick script to check product image URLs in database vs API response
FIXED: Now properly loads environment variables
"""
import os
import sys
from pathlib import Path
import json

# Load environment variables BEFORE Django setup
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'

print(f"Loading environment from: {env_path}")
if not env_path.exists():
    print("ERROR: .env file not found!")
    sys.exit(1)

load_dotenv(env_path)

# Setup Django
import django
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings.dev')

try:
    django.setup()
except Exception as e:
    print(f"ERROR setting up Django: {e}")
    sys.exit(1)

from apps.products.models import Product
from apps.products.serializers import ProductListSerializer
from django.test import RequestFactory

print("=" * 80)
print("PRODUCT IMAGE URL DIAGNOSTIC")
print("=" * 80)

# Get first 5 products
products = Product.objects.all()[:5]

if not products:
    print("\n❌ No products found in database!")
    print("   You need to create products first through Django admin.")
    sys.exit(1)

# Create a mock request for the serializer
factory = RequestFactory()
request = factory.get('/')
request.META['HTTP_HOST'] = 'localhost:8000'
request.META['wsgi.url_scheme'] = 'http'

print(f"\nFound {Product.objects.count()} products in database")
print("\nChecking first 5 products:\n")

for i, product in enumerate(products, 1):
    print(f"{i}. Product: {product.name}")
    print(f"   ID: {product.id}")
    
    # Check the raw database field
    print(f"\n   📁 Database Field:")
    if product.featured_image and product.featured_image.name:
        print(f"   - Field Name: {product.featured_image.name}")
        try:
            url = product.featured_image.url
            print(f"   - Generated URL: {url}")
            
            # Check if it's a Cloudinary URL
            if 'cloudinary' in url:
                print(f"   - ✅ Cloudinary URL detected")
            elif '/media/' in url:
                print(f"   - ⚠️  Local media URL (not Cloudinary)")
            else:
                print(f"   - ❓ Unknown URL format")
        except Exception as e:
            print(f"   - ❌ Error generating URL: {e}")
    else:
        print(f"   - ❌ No image set (field is empty)")
    
    # Check the serialized output
    print(f"\n   📤 API Response (Serialized):")
    serializer = ProductListSerializer(product, context={'request': request})
    serialized_data = serializer.data
    
    if serialized_data.get('featured_image'):
        print(f"   - URL: {serialized_data['featured_image']}")
        if 'cloudinary' in serialized_data['featured_image']:
            print(f"   - ✅ Will show Cloudinary URL in API")
        else:
            print(f"   - ⚠️  Will show local URL in API")
    else:
        print(f"   - ❌ featured_image is null in API response")
    
    print(f"\n   Full serialized product:")
    print(f"   {json.dumps(serialized_data, indent=2, default=str)}")
    print("\n" + "-" * 80 + "\n")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

# Count products with images
products_with_images = Product.objects.exclude(featured_image='').count()
total_products = Product.objects.count()

print(f"\nProducts with images: {products_with_images}/{total_products}")

if products_with_images == 0:
    print("\n⚠️  ISSUE: No products have images uploaded!")
    print("   Solution: Add images to your products through Django admin")
else:
    # Check if any are Cloudinary URLs
    cloudinary_count = 0
    local_count = 0
    
    for product in Product.objects.exclude(featured_image=''):
        if product.featured_image and product.featured_image.name:
            try:
                if 'cloudinary' in product.featured_image.url:
                    cloudinary_count += 1
                else:
                    local_count += 1
            except:
                pass
    
    print(f"\n   - Cloudinary images: {cloudinary_count}")
    print(f"   - Local images: {local_count}")
    
    if local_count > 0:
        print("\n⚠️  ISSUE: Some images are stored locally, not in Cloudinary!")
        print("   This means they were uploaded before Cloudinary was configured.")
        print("   Solution: Re-upload the images through Django admin, or migrate them")
    
    if cloudinary_count > 0:
        print("\n✅ SUCCESS: Found Cloudinary images!")
        print("   If images still don't show on frontend, check:")
        print("   1. Browser console for errors")
        print("   2. Network tab to see actual API response")
        print("   3. Frontend code is correctly reading the featured_image field")

print("\n" + "=" * 80)
