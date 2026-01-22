"""
Script to check if images are uploaded to Cloudinary
FIXED: Now properly loads environment variables
"""
import os
import sys
from pathlib import Path

# Load environment variables from .env file BEFORE Django setup
from dotenv import load_dotenv

# Get the backend directory
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'

print(f"Loading environment from: {env_path}")
print(f"File exists: {env_path.exists()}")

if not env_path.exists():
    print("ERROR: .env file not found!")
    sys.exit(1)

# Load the .env file
load_dotenv(env_path)

# Verify variables are loaded
print("\nEnvironment variables loaded:")
print(f"CLOUDINARY_CLOUD_NAME: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
print(f"CLOUDINARY_API_KEY: {os.getenv('CLOUDINARY_API_KEY')}")
print(f"CLOUDINARY_API_SECRET: {'*' * 20 if os.getenv('CLOUDINARY_API_SECRET') else 'NOT SET'}")
print(f"DATABASE_URL: {'SET' if os.getenv('DATABASE_URL') else 'NOT SET'}")
print(f"CORS_ALLOWED_ORIGINS: {os.getenv('CORS_ALLOWED_ORIGINS')}")

# Now setup Django
import django
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings.dev')

try:
    django.setup()
except Exception as e:
    print(f"\nERROR setting up Django: {e}")
    sys.exit(1)

from apps.products.models import Product, ProductImage
import cloudinary
import cloudinary.api

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

print("\n" + "=" * 80)
print("CLOUDINARY CHECK")
print("=" * 80)

# Check Cloudinary configuration
print("\n1. Cloudinary Configuration:")
print(f"   Cloud Name: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
print(f"   API Key: {os.getenv('CLOUDINARY_API_KEY')}")
print(f"   API Secret: {'*' * 10}{os.getenv('CLOUDINARY_API_SECRET')[-4:]}")

# Check products in database
print("\n2. Products in Database:")
products = Product.objects.all()[:5]

if not products:
    print("   No products found in database!")
else:
    for product in products:
        print(f"\n   Product: {product.name}")
        print(f"   - ID: {product.id}")
        print(f"   - Featured Image Field: {product.featured_image}")
        print(f"   - Featured Image Name: {product.featured_image.name if product.featured_image else 'None'}")
        
        if product.featured_image and product.featured_image.name:
            try:
                print(f"   - Image URL: {product.featured_image.url}")
            except Exception as e:
                print(f"   - Error getting URL: {e}")
        else:
            print(f"   - No featured image set")
        
        # Check additional images
        images = product.images.all()
        if images:
            print(f"   - Additional Images: {images.count()}")
            for img in images:
                print(f"     - {img.image.name if img.image else 'None'}")

# Try to list all images in Cloudinary
print("\n3. Images in Cloudinary:")
try:
    result = cloudinary.api.resources(
        type="upload",
        prefix="products/",
        max_results=10
    )
    
    if result['resources']:
        print(f"   Found {len(result['resources'])} images in 'products/' folder:")
        for resource in result['resources']:
            print(f"   - {resource['public_id']}")
            print(f"     URL: {resource['secure_url']}")
    else:
        print("   No images found in 'products/' folder")
    
    # Also check root level
    root_result = cloudinary.api.resources(
        type="upload",
        max_results=10
    )
    print(f"\n   Total images in Cloudinary: {root_result['total_count']}")
    
except Exception as e:
    print(f"   Error accessing Cloudinary: {e}")

print("\n" + "=" * 80)
print("CHECK COMPLETE")
print("=" * 80)
