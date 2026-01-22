"""
Simple script to verify Django is loading environment variables correctly
"""
from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'
load_dotenv(env_path)

print("=" * 80)
print("ENVIRONMENT VARIABLE CHECK")
print("=" * 80)

print(f"\n.env file location: {env_path}")
print(f".env file exists: {env_path.exists()}")

print("\n📋 Checking key environment variables:")

vars_to_check = [
    'DATABASE_URL',
    'CLOUDINARY_CLOUD_NAME',
    'CLOUDINARY_API_KEY',
    'CLOUDINARY_API_SECRET',
    'CORS_ALLOWED_ORIGINS',
    'SECRET_KEY',
]

all_set = True
for var in vars_to_check:
    value = os.getenv(var)
    if value:
        if 'SECRET' in var or 'KEY' in var:
            display = f"{'*' * 20}...{value[-4:]}" if len(value) > 4 else "***"
        else:
            display = value if len(value) < 50 else value[:47] + "..."
        print(f"  ✅ {var}: {display}")
    else:
        print(f"  ❌ {var}: NOT SET")
        all_set = False

if all_set:
    print("\n✅ All environment variables are set!")
    print("\nNow testing Django setup...")
    
    # Try to setup Django
    import sys
    import django
    
    sys.path.insert(0, str(BASE_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings.dev')
    
    try:
        django.setup()
        from django.conf import settings
        
        print("\n✅ Django setup successful!")
        print(f"\n📦 Storage Backend: {settings.STORAGES['default']['BACKEND']}")
        
        if 'cloudinary' in settings.STORAGES['default']['BACKEND'].lower():
            print("✅ Using Cloudinary storage!")
        else:
            print("⚠️  Not using Cloudinary storage")
        
        # Try to import and check a product
        from apps.products.models import Product
        product_count = Product.objects.count()
        print(f"\n📊 Products in database: {product_count}")
        
        if product_count > 0:
            # Check first product
            product = Product.objects.first()
            print(f"\n🔍 Checking first product: {product.name}")
            if product.featured_image and product.featured_image.name:
                print(f"   Image field: {product.featured_image.name}")
                try:
                    url = product.featured_image.url
                    print(f"   Image URL: {url}")
                    if 'cloudinary' in url:
                        print("   ✅ URL is from Cloudinary!")
                    else:
                        print("   ⚠️  URL is NOT from Cloudinary")
                except Exception as e:
                    print(f"   ❌ Error getting URL: {e}")
            else:
                print("   ⚠️  No image uploaded")
        
    except Exception as e:
        print(f"\n❌ Django setup failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n❌ Some environment variables are missing!")
    print("   Check your .env file")

print("\n" + "=" * 80)
