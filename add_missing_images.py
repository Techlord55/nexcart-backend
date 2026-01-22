"""
Find products without images and fix them
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

print("=" * 80)
print("FIND PRODUCTS WITHOUT IMAGES")
print("=" * 80)

# Find products without images
products_without_images = []
for product in Product.objects.all():
    if not product.featured_image or not product.featured_image.name:
        products_without_images.append(product)
        print(f"\n❌ {product.name}")
        print(f"   Category: {product.category.name if product.category else 'No category'}")
        print(f"   ID: {product.id}")

if not products_without_images:
    print("\n✅ All products have images!")
    sys.exit(0)

print(f"\n\nFound {len(products_without_images)} products without images")
print("\n" + "=" * 80)

# Default placeholder images for different categories
category_images = {
    'Kitchenware': 'https://images.unsplash.com/photo-1556908153-e449f7fa7f0d?w=800&q=80',  # Kitchen items
    'Books': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&q=80',  # Books
    'Clothing': 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=800&q=80',  # Clothing
    'Electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800&q=80',  # Electronics
    'Home & Living': 'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=800&q=80',  # Home
}

# Generic fallback
default_image = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80'

print("\nAttempting to add appropriate images based on category...")
print("-" * 80)

success_count = 0
fail_count = 0

for i, product in enumerate(products_without_images, 1):
    print(f"\n[{i}/{len(products_without_images)}] {product.name}")
    
    # Choose appropriate image based on category
    category_name = product.category.name if product.category else 'Unknown'
    image_url = category_images.get(category_name, default_image)
    
    print(f"   Category: {category_name}")
    print(f"   Using image: {image_url}")
    
    try:
        # Download the image
        print(f"   Downloading...")
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Get file extension
        ext = 'jpg'
        
        # Create a filename
        filename = f"{product.slug}.{ext}"
        
        # Save the file to the ImageField
        print(f"   Uploading to Cloudinary...")
        product.featured_image.save(
            filename,
            ContentFile(response.content),
            save=True
        )
        
        print(f"   ✅ Success! New URL: {product.featured_image.url}")
        success_count += 1
        
        # Small delay to avoid rate limiting
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

print("\n🎉 Done! Check http://localhost:3000/products to see all products with images.")
print("\n" + "=" * 80)
