"""
Fix products that have external URLs instead of uploaded images
Downloads the external images and re-uploads them properly to Cloudinary
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
print("FIX EXTERNAL IMAGE URLs")
print("=" * 80)

# Find products with external URLs
products_to_fix = []
for product in Product.objects.all():
    if product.featured_image and product.featured_image.name:
        if 'http' in product.featured_image.name:
            products_to_fix.append(product)

if not products_to_fix:
    print("\n✅ No products need fixing! All images are properly uploaded.")
    sys.exit(0)

print(f"\n Found {len(products_to_fix)} products with external URLs")
print(f"\nThis will:")
print(f"  1. Download each external image")
print(f"  2. Upload it properly to Cloudinary")
print(f"  3. Update the product with the new Cloudinary URL")

response = input(f"\nProceed? (yes/no): ")
if response.lower() != 'yes':
    print("Cancelled.")
    sys.exit(0)

print("\n" + "-" * 80)
print("Processing products...")
print("-" * 80)

success_count = 0
fail_count = 0

for i, product in enumerate(products_to_fix, 1):
    print(f"\n[{i}/{len(products_to_fix)}] {product.name}")
    
    # Get the external URL
    external_url = product.featured_image.name
    print(f"   External URL: {external_url}")
    
    try:
        # Download the image
        print(f"   Downloading...")
        response = requests.get(external_url, timeout=10)
        response.raise_for_status()
        
        # Get file extension from URL or default to jpg
        ext = 'jpg'
        if '.' in external_url.split('?')[0]:
            ext = external_url.split('?')[0].split('.')[-1]
            if ext not in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                ext = 'jpg'
        
        # Create a filename
        filename = f"{product.slug}.{ext}"
        
        # Save the file to the ImageField
        # This will automatically upload to Cloudinary
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
print(f"\n✅ Successfully fixed: {success_count} products")
if fail_count > 0:
    print(f"❌ Failed: {fail_count} products")

print("\n🎉 Done! Your images should now display properly on the frontend.")
print("   Visit http://localhost:3000/products to verify.")
print("\n" + "=" * 80)
