"""
Check current status of all products and their images
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

print("=" * 80)
print("CURRENT PRODUCT IMAGE STATUS")
print("=" * 80)

all_products = Product.objects.all().order_by('name')
products_with_images = 0
products_without_images = []

for product in all_products:
    if product.featured_image and product.featured_image.name:
        products_with_images += 1
        status = "✅"
    else:
        products_without_images.append(product)
        status = "❌"
    
    print(f"{status} {product.name}")
    if not (product.featured_image and product.featured_image.name):
        print(f"   ID: {product.id}")
        print(f"   Category: {product.category.name if product.category else 'No category'}")

print("\n" + "=" * 80)
print(f"Total products: {all_products.count()}")
print(f"With images: {products_with_images}")
print(f"Without images: {len(products_without_images)}")
print("=" * 80)

if products_without_images:
    print(f"\n❌ {len(products_without_images)} products need images:")
    for p in products_without_images:
        print(f"   - {p.name} (Category: {p.category.name if p.category else 'None'})")
