"""
Fix products that still have external URLs with working images
"""
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

import django
import sys
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings.dev')
django.setup()

from apps.products.models import Product
from django.core.files.base import ContentFile
import requests

# Working images for products that need them
WORKING_IMAGES = {
    'non-stick-cookware-set': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
    'kitchen-knife-set': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=800&q=80',
}

print("=" * 80)
print("FIX PRODUCTS WITH BROKEN EXTERNAL URLs")
print("=" * 80)

# Find products that still have 'http' in their featured_image.name
broken_products = []
for product in Product.objects.all():
    if product.featured_image and product.featured_image.name:
        if 'http' in product.featured_image.name:
            broken_products.append(product)
            print(f"\n❌ {product.name}")
            print(f"   Current: {product.featured_image.name}")

if not broken_products:
    print("\n✅ No products with external URLs found!")
    sys.exit(0)

print(f"\n\nFixing {len(broken_products)} products...")
print("-" * 80)

for product in broken_products:
    print(f"\n📦 {product.name}")
    
    # Get a working image URL
    image_url = WORKING_IMAGES.get(product.slug)
    
    if not image_url:
        # Use a generic high-quality image based on category
        if product.category:
            if 'kitchen' in product.category.name.lower() or 'home' in product.category.name.lower():
                image_url = 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80'
            elif 'clothing' in product.category.name.lower():
                image_url = 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800&q=80'
            elif 'electronics' in product.category.name.lower():
                image_url = 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800&q=80'
            else:
                image_url = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80'
        else:
            image_url = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80'
    
    print(f"   Using: {image_url}")
    
    try:
        # Download the image
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Save it properly
        filename = f"{product.slug}.jpg"
        product.featured_image.save(
            filename,
            ContentFile(response.content),
            save=True
        )
        
        print(f"   ✅ Fixed! New URL: {product.featured_image.url}")
        
    except Exception as e:
        print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("🎉 Done! All products should now have proper Cloudinary images.")
print("=" * 80)
