"""
Create sample products for testing
"""
from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.products.models import Category, Product


class Command(BaseCommand):
    help = 'Create sample products for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample products...')

        # Create categories
        electronics, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={
                'slug': 'electronics',
                'description': 'Electronic devices and gadgets',
                'is_active': True
            }
        )

        clothing, _ = Category.objects.get_or_create(
            name='Clothing',
            defaults={
                'slug': 'clothing',
                'description': 'Fashion and apparel',
                'is_active': True
            }
        )

        home, _ = Category.objects.get_or_create(
            name='Home & Garden',
            defaults={
                'slug': 'home-garden',
                'description': 'Home and garden products',
                'is_active': True
            }
        )

        books, _ = Category.objects.get_or_create(
            name='Books',
            defaults={
                'slug': 'books',
                'description': 'Books and reading materials',
                'is_active': True
            }
        )

        # Sample products
        products_data = [
            # Electronics
            {
                'name': 'Wireless Bluetooth Headphones',
                'category': electronics,
                'description': 'Premium wireless headphones with active noise cancellation and 30-hour battery life.',
                'price': Decimal('89.99'),
                'compare_price': Decimal('129.99'),
                'sku': 'WBH-001',
                'stock_quantity': 50,
                'is_featured': True,
                'tags': 'audio, wireless, bluetooth, headphones',
            },
            {
                'name': 'Smart Watch Pro',
                'category': electronics,
                'description': 'Advanced smartwatch with fitness tracking, heart rate monitor, and GPS.',
                'price': Decimal('199.99'),
                'compare_price': Decimal('249.99'),
                'sku': 'SWP-001',
                'stock_quantity': 30,
                'is_featured': True,
                'tags': 'smartwatch, fitness, wearable, electronics',
            },
            {
                'name': 'Portable Power Bank 20000mAh',
                'category': electronics,
                'description': 'High-capacity portable charger with fast charging support for all devices.',
                'price': Decimal('34.99'),
                'compare_price': Decimal('49.99'),
                'sku': 'PPB-001',
                'stock_quantity': 100,
                'is_featured': False,
                'tags': 'power bank, charger, portable, battery',
            },
            {
                'name': 'Wireless Gaming Mouse',
                'category': electronics,
                'description': 'Precision gaming mouse with RGB lighting and programmable buttons.',
                'price': Decimal('59.99'),
                'compare_price': Decimal('79.99'),
                'sku': 'WGM-001',
                'stock_quantity': 75,
                'is_featured': True,
                'tags': 'gaming, mouse, wireless, rgb',
            },
            
            # Clothing
            {
                'name': 'Classic Cotton T-Shirt',
                'category': clothing,
                'description': 'Comfortable 100% cotton t-shirt available in multiple colors.',
                'price': Decimal('19.99'),
                'compare_price': Decimal('29.99'),
                'sku': 'CCT-001',
                'stock_quantity': 200,
                'is_featured': False,
                'tags': 'tshirt, cotton, casual, clothing',
            },
            {
                'name': 'Premium Denim Jeans',
                'category': clothing,
                'description': 'High-quality denim jeans with perfect fit and durability.',
                'price': Decimal('69.99'),
                'compare_price': Decimal('99.99'),
                'sku': 'PDJ-001',
                'stock_quantity': 80,
                'is_featured': True,
                'tags': 'jeans, denim, pants, clothing',
            },
            {
                'name': 'Running Shoes',
                'category': clothing,
                'description': 'Lightweight running shoes with excellent cushioning and support.',
                'price': Decimal('89.99'),
                'compare_price': Decimal('119.99'),
                'sku': 'RS-001',
                'stock_quantity': 60,
                'is_featured': True,
                'tags': 'shoes, running, sports, footwear',
            },
            {
                'name': 'Winter Jacket',
                'category': clothing,
                'description': 'Warm and waterproof winter jacket for cold weather.',
                'price': Decimal('129.99'),
                'compare_price': Decimal('179.99'),
                'sku': 'WJ-001',
                'stock_quantity': 40,
                'is_featured': False,
                'tags': 'jacket, winter, outerwear, clothing',
            },
            
            # Home & Garden
            {
                'name': 'Stainless Steel Coffee Maker',
                'category': home,
                'description': 'Programmable coffee maker with thermal carafe and auto-shutoff.',
                'price': Decimal('79.99'),
                'compare_price': Decimal('99.99'),
                'sku': 'SSCM-001',
                'stock_quantity': 45,
                'is_featured': True,
                'tags': 'coffee maker, kitchen, appliance, home',
            },
            {
                'name': 'Memory Foam Pillow Set',
                'category': home,
                'description': 'Set of 2 ergonomic memory foam pillows for better sleep.',
                'price': Decimal('49.99'),
                'compare_price': Decimal('69.99'),
                'sku': 'MFP-001',
                'stock_quantity': 90,
                'is_featured': False,
                'tags': 'pillow, bedroom, sleep, home',
            },
            {
                'name': 'LED Desk Lamp',
                'category': home,
                'description': 'Adjustable LED desk lamp with touch controls and USB charging port.',
                'price': Decimal('39.99'),
                'compare_price': Decimal('54.99'),
                'sku': 'LDL-001',
                'stock_quantity': 70,
                'is_featured': False,
                'tags': 'lamp, led, desk, lighting, home',
            },
            
            # Books
            {
                'name': 'The Complete Python Guide',
                'category': books,
                'description': 'Comprehensive guide to Python programming for beginners and experts.',
                'price': Decimal('39.99'),
                'compare_price': Decimal('49.99'),
                'sku': 'CPG-001',
                'stock_quantity': 100,
                'is_featured': True,
                'tags': 'python, programming, coding, books, education',
            },
            {
                'name': 'Modern Web Development',
                'category': books,
                'description': 'Learn modern web development with React, Node.js, and more.',
                'price': Decimal('44.99'),
                'compare_price': Decimal('59.99'),
                'sku': 'MWD-001',
                'stock_quantity': 85,
                'is_featured': False,
                'tags': 'web development, react, nodejs, books, programming',
            },
        ]

        created_count = 0
        updated_count = 0

        for product_data in products_data:
            product, created = Product.objects.update_or_create(
                sku=product_data['sku'],
                defaults=product_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {product.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Updated: {product.name}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nComplete! Created {created_count} new products, updated {updated_count} existing products.'
        ))
