"""
Fix the Non-Stick Cookware Set image specifically
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

print("=" * 80)
print("FIX NON-STICK COOKWARE SET IMAGE")
print("=" * 80)

# Get the product
product = Product.objects.filter(name="Non-Stick Cookware Set").first()

if not product:
    print("Product not found!")
    sys.exit(1)

print(f"\nProduct: {product.name}")
print(f"Current image: {product.featured_image.name if product.featured_image else 'None'}")

# Use a high-quality cookware image
image_url = 'https://images.unsplash.com/photo-1584990347449-39b4aa02b01f?w=800&q=80'

print(f"\nDownloading new image from: {image_url}")

try:
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()
    
    # Save the image
    product.featured_image.save(
        'non-stick-cookware-set.jpg',
        ContentFile(response.content),
        save=True
    )
    
    print(f"\n✅ Success!")
    print(f"New image URL: {product.featured_image.url}")
    
except Exception as e:
    print(f"\n❌ Failed: {e}")

print("\n" + "=" * 80)
