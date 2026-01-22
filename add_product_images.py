"""
Add appropriate images to products that are missing them
Uses product-specific high-quality images
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
import time

# High-quality product images mapped by product name/category
PRODUCT_IMAGES = {
    # Kitchenware
    'non-stick cookware set': 'https://images.unsplash.com/photo-1584990347449-39b4aa02b01f?w=800&q=80',
    'kitchen knife set': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=800&q=80',
    'stainless steel coffee maker': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&q=80',
    
    # Clothing
    'cotton t-shirt pack': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80',
    'winter jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80',
    'running shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80',
    'premium denim jeans': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&q=80',
    
    # Electronics
    'led desk lamp': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&q=80',
    'wireless gaming mouse': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80',
    'portable power bank 20000mah': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800&q=80',
    'smart watch pro': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80',
    'wireless bluetooth headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
    'mechanical keyboard': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80',
    'usb-c hub adapter': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&q=80',
    '4k webcam': 'https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=800&q=80',
    
    # Books
    'modern web development': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&q=80',
    'the complete python guide': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&q=80',
    
    # Home & Living
    'memory foam pillow set': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80',
    'yoga mat': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800&q=80',
    'ceramic plant pot': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=800&q=80',
}

# Category fallback images
CATEGORY_FALLBACKS = {
    'Kitchenware': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
    'Home & Garden': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
    'Books': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=800&q=80',
    'Clothing': 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800&q=80',
    'Electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800&q=80',
    'Home & Living': 'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=800&q=80',
}

# Generic fallback
DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1560393464-5c69a73c5770?w=800&q=80'

print("=" * 80)
print("ADD IMAGES TO PRODUCTS WITHOUT THEM")
print("=" * 80)

# Find products without images
products_without_images = []
for product in Product.objects.all():
    if not product.featured_image or not product.featured_image.name:
        products_without_images.append(product)

if not products_without_images:
    print("\n✅ All products already have images!")
    sys.exit(0)

print(f"\nFound {len(products_without_images)} products without images:\n")
for p in products_without_images:
    print(f"   - {p.name} (Category: {p.category.name if p.category else 'None'})")

response = input(f"\nAdd images to these {len(products_without_images)} products? (yes/no): ")
if response.lower() != 'yes':
    print("Cancelled.")
    sys.exit(0)

print("\n" + "-" * 80)
print("Processing...")
print("-" * 80)

success_count = 0
fail_count = 0

for i, product in enumerate(products_without_images, 1):
    print(f"\n[{i}/{len(products_without_images)}] {product.name}")
    
    # Try to find a specific image for this product
    product_key = product.name.lower().strip()
    image_url = PRODUCT_IMAGES.get(product_key)
    
    if not image_url:
        # Try category fallback
        category_name = product.category.name if product.category else None
        image_url = CATEGORY_FALLBACKS.get(category_name, DEFAULT_IMAGE)
        print(f"   Using category fallback image ({category_name})")
    else:
        print(f"   Using product-specific image")
    
    print(f"   Image URL: {image_url}")
    
    try:
        # Download the image
        print(f"   Downloading...")
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Create filename
        filename = f"{product.slug}.jpg"
        
        # Save to Cloudinary
        print(f"   Uploading to Cloudinary...")
        product.featured_image.save(
            filename,
            ContentFile(response.content),
            save=True
        )
        
        print(f"   ✅ Success! URL: {product.featured_image.url}")
        success_count += 1
        
        # Delay to avoid rate limiting
        time.sleep(0.5)
        
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        fail_count += 1

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\n✅ Successfully added images: {success_count} products")
if fail_count > 0:
    print(f"❌ Failed: {fail_count} products")

print("\n🎉 Done! All products should now have images.")
print("   Visit http://localhost:3000/products to verify.")
print("\n" + "=" * 80)
