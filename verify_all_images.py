"""
Final verification - check all products have proper images
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

from apps.products.models import Product, ProductImage

print("=" * 80)
print("FINAL IMAGE VERIFICATION")
print("=" * 80)

all_good = True

for product in Product.objects.all().order_by('name'):
    print(f"\n📦 {product.name}")
    
    # Check featured image
    if not product.featured_image or not product.featured_image.name:
        print(f"   ❌ No featured image!")
        all_good = False
    elif 'http' in product.featured_image.name and 'cloudinary' not in product.featured_image.name:
        print(f"   ⚠️  Featured image is external URL: {product.featured_image.name}")
        all_good = False
    else:
        # Check if it's a proper Cloudinary URL
        try:
            url = product.featured_image.url
            if 'cloudinary' in url:
                print(f"   ✅ Featured image: Cloudinary ✓")
            else:
                print(f"   ⚠️  Featured image: {url}")
                all_good = False
        except Exception as e:
            print(f"   ❌ Error getting URL: {e}")
            all_good = False
    
    # Check additional images
    additional_images = product.images.count()
    if additional_images > 0:
        print(f"   ✅ Gallery images: {additional_images}")
    else:
        print(f"   ⚠️  No gallery images")

print("\n" + "=" * 80)
if all_good:
    print("✅ ALL PRODUCTS HAVE PROPER CLOUDINARY IMAGES!")
else:
    print("⚠️  Some products still need attention (see above)")
print("=" * 80)

# Summary
total_products = Product.objects.count()
products_with_featured = Product.objects.exclude(featured_image='').count()
products_with_gallery = Product.objects.filter(images__isnull=False).distinct().count()
total_gallery_images = ProductImage.objects.count()

print(f"\n📊 Summary:")
print(f"   Total products: {total_products}")
print(f"   With featured images: {products_with_featured}/{total_products}")
print(f"   With gallery images: {products_with_gallery}/{total_products}")
print(f"   Total gallery images: {total_gallery_images}")

print("\n" + "=" * 80)
