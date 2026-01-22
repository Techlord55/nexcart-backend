"""
Add multiple product images (gallery) for each product
Each product will get 3-4 additional images beyond the featured image
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
from django.core.files.base import ContentFile
import requests
import time

# Product gallery images - multiple images per product
PRODUCT_GALLERIES = {
    'non-stick-cookware-set': [
        'https://images.unsplash.com/photo-1584990347449-39b4aa02b01f?w=800&q=80',
        'https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=800&q=80',
        'https://images.unsplash.com/photo-1585515320310-259814833298?w=800&q=80',
    ],
    'kitchen-knife-set': [
        'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=800&q=80',
        'https://images.unsplash.com/photo-1593618998111-15c68c2e9e80?w=800&q=80',
        'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=800&q=80',
    ],
    'cotton-t-shirt-pack': [
        'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80',
        'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&q=80',
        'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&q=80',
    ],
    'modern-web-development': [
        'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&q=80',
        'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=800&q=80',
        'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800&q=80',
    ],
    'the-complete-python-guide': [
        'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&q=80',
        'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&q=80',
        'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&q=80',
    ],
    'led-desk-lamp': [
        'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&q=80',
        'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=800&q=80',
        'https://images.unsplash.com/photo-1545127398-14699f92334b?w=800&q=80',
    ],
    'stainless-steel-coffee-maker': [
        'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&q=80',
        'https://images.unsplash.com/photo-1511920170033-f8396924c348?w=800&q=80',
        'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80',
    ],
    'winter-jacket': [
        'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80',
        'https://images.unsplash.com/photo-1544923408-75c5cef46f14?w=800&q=80',
        'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=800&q=80',
    ],
    'running-shoes': [
        'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80',
        'https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=800&q=80',
        'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=800&q=80',
    ],
    'premium-denim-jeans': [
        'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&q=80',
        'https://images.unsplash.com/photo-1475178626620-a4d074967452?w=800&q=80',
        'https://images.unsplash.com/photo-1582552938357-32b906df40cb?w=800&q=80',
    ],
    'wireless-gaming-mouse': [
        'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80',
        'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&q=80',
        'https://images.unsplash.com/photo-1563297007-0686b7003af7?w=800&q=80',
    ],
    'portable-power-bank-20000mah': [
        'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800&q=80',
        'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&q=80',
        'https://images.unsplash.com/photo-1591290619762-ece3819b8e2e?w=800&q=80',
    ],
    'smart-watch-pro': [
        'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80',
        'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800&q=80',
        'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&q=80',
    ],
    'wireless-bluetooth-headphones': [
        'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
        'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800&q=80',
        'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&q=80',
    ],
    'memory-foam-pillow-set': [
        'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80',
        'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&q=80',
        'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=800&q=80',
    ],
    'classic-cotton-t-shirt': [
        'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80',
        'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800&q=80',
        'https://images.unsplash.com/photo-1622445275463-afa2ab738c34?w=800&q=80',
    ],
}

print("=" * 80)
print("ADD PRODUCT GALLERY IMAGES")
print("=" * 80)

products = Product.objects.all()
total_images_added = 0

for product in products:
    print(f"\n📦 {product.name}")
    print(f"   Slug: {product.slug}")
    
    # Check if product already has additional images
    existing_images = product.images.count()
    if existing_images >= 3:
        print(f"   ✅ Already has {existing_images} additional images - skipping")
        continue
    
    # Get gallery images for this product
    gallery_urls = PRODUCT_GALLERIES.get(product.slug, [])
    
    if not gallery_urls:
        print(f"   ⚠️  No gallery images defined for this product")
        continue
    
    print(f"   Adding {len(gallery_urls)} gallery images...")
    
    for position, image_url in enumerate(gallery_urls, start=1):
        try:
            # Download image
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Create ProductImage
            product_image = ProductImage(
                product=product,
                alt_text=f"{product.name} - Image {position}",
                position=position
            )
            
            # Save image to Cloudinary
            filename = f"{product.slug}-{position}.jpg"
            product_image.image.save(
                filename,
                ContentFile(response.content),
                save=True
            )
            
            print(f"   ✅ Added image {position}: {product_image.image.url}")
            total_images_added += 1
            
            time.sleep(0.3)  # Rate limiting
            
        except Exception as e:
            print(f"   ❌ Failed to add image {position}: {e}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\n✅ Total gallery images added: {total_images_added}")
print("\n🎉 Done! Products now have image galleries.")
print("   Visit product detail pages to see the galleries.")
print("\n" + "=" * 80)
