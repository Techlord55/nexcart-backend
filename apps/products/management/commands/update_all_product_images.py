"""
Simply update ALL existing products with image URLs based on their names
"""
from django.core.management.base import BaseCommand
from apps.products.models import Product


class Command(BaseCommand):
    help = 'Update all existing products with Unsplash image URLs'

    def handle(self, *args, **options):
        self.stdout.write('Updating all products with image URLs...')

        # Map product names to Unsplash image URLs
        # These are free-to-use stock photos from Unsplash
        product_images = {
            # Electronics
            'wireless bluetooth headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
            'smart watch pro': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80',
            'portable power bank 20000mah': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800&q=80',
            'wireless gaming mouse': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80',
            
            # Clothing
            'premium denim jeans': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&q=80',
            'cotton t-shirt pack': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80',
            'winter jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80',
            'running shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80',
            
            # Home & Garden
            'stainless steel coffee maker': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&q=80',
            'led desk lamp': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&q=80',
            'kitchen knife set': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=800&q=80',
            'non-stick cookware set': 'https://images.unsplash.com/photo-1556908153-619b8c9d8be4?w=800&q=80',
            
            # Books (match various possible names)
            'the complete python guide': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&q=80',
            'python programming guide': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&q=80',
            'modern web development': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&q=80',
            'web development masterclass': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&q=80',
            'data science handbook': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=800&q=80',
            'data science essentials': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=800&q=80',
            'digital marketing essentials': 'https://images.unsplash.com/photo-1533750204176-3b0d38e9ac2d?w=800&q=80',
            'marketing strategy guide': 'https://images.unsplash.com/photo-1533750204176-3b0d38e9ac2d?w=800&q=80',
        }

        updated_count = 0
        not_matched = []
        
        # Get all products
        all_products = Product.objects.all()
        
        for product in all_products:
            product_name_lower = product.name.lower()
            
            # Try to find a matching image
            image_url = product_images.get(product_name_lower)
            
            if image_url:
                product.featured_image = image_url
                product.save(update_fields=['featured_image'])
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Updated: {product.name}')
                )
            else:
                not_matched.append(product.name)
                self.stdout.write(
                    self.style.WARNING(f'⚠ No image found for: {product.name}')
                )

        # Summary
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(f'✓ Updated {updated_count} products with image URLs')
        )
        
        if not_matched:
            self.stdout.write('')
            self.stdout.write(
                self.style.WARNING(f'⚠ {len(not_matched)} products without images:')
            )
            for name in not_matched:
                self.stdout.write(f'  - {name}')
