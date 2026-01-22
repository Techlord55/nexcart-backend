"""
Add sample images to products using Unsplash URLs
"""
from django.core.management.base import BaseCommand
from apps.products.models import Product


class Command(BaseCommand):
    help = 'Add sample images to products using Unsplash URLs'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample images to products...')

        # Sample Unsplash image URLs (these are free to use)
        product_images = {
            'Wireless Bluetooth Headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800',
            'Smart Watch Pro': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800',
            'Portable Power Bank 20000mAh': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800',
            'Wireless Gaming Mouse': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800',
            'Premium Denim Jeans': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800',
            'Cotton T-Shirt Pack': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800',
            'Winter Jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800',
            'Running Shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800',
            'Stainless Steel Coffee Maker': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800',
            'LED Desk Lamp': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800',
            'Kitchen Knife Set': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=800',
            'Non-Stick Cookware Set': 'https://images.unsplash.com/photo-1556908153-619b8c9d8be4?w=800',
            'The Complete Python Guide': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800',
            'Modern Web Development': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800',
            'Data Science Handbook': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=800',
            'Digital Marketing Essentials': 'https://images.unsplash.com/photo-1533750204176-3b0d38e9ac2d?w=800',
        }

        updated_count = 0
        for product_name, image_url in product_images.items():
            try:
                product = Product.objects.get(name=product_name)
                # Store the URL in the featured_image field
                # Note: This stores the URL as text, not uploading the actual file
                product.featured_image = image_url
                product.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Updated image for: {product_name}')
                )
            except Product.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'✗ Product not found: {product_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully updated {updated_count} products')
        )
