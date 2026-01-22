"""
QUICK FIX: Update create_sample_products to include Unsplash image URLs
This approach stores URLs directly in the ImageField (works in Django)
"""
from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.products.models import Category, Product


class Command(BaseCommand):
    help = 'Create sample products with Unsplash images'

    def handle(self, *args, **options):
        self.stdout.write('Creating/Updating sample products with images...')

        # Create categories first
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

        # Sample products with Unsplash images
        products_data = [
            {
                'name': 'Wireless Bluetooth Headphones',
                'category': electronics,
                'description': 'Premium wireless headphones with active noise cancellation.',
                'price': Decimal('89.99'),
                'compare_price': Decimal('129.99'),
                'sku': 'WBH-001',
                'stock_quantity': 50,
                'is_featured': True,
                'featured_image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
            },
            {
                'name': 'Smart Watch Pro',
                'category': electronics,
                'description': 'Advanced smartwatch with fitness tracking.',
                'price': Decimal('199.99'),
                'compare_price': Decimal('249.99'),
                'sku': 'SWP-001',
                'stock_quantity': 30,
                'is_featured': True,
                'featured_image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80',
            },
            {
                'name': 'Portable Power Bank 20000mAh',
                'category': electronics,
                'description': 'High-capacity portable charger.',
                'price': Decimal('34.99'),
                'compare_price': Decimal('49.99'),
                'sku': 'PPB-001',
                'stock_quantity': 100,
                'is_featured': False,
                'featured_image': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800&q=80',
            },
            {
                'name': 'Wireless Gaming Mouse',
                'category': electronics,
                'description': 'Precision gaming mouse with RGB lighting.',
                'price': Decimal('59.99'),
                'compare_price': Decimal('79.99'),
                'sku': 'WGM-001',
                'stock_quantity': 75,
                'is_featured': True,
                'featured_image': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80',
            },
            {
                'name': 'Premium Denim Jeans',
                'category': clothing,
                'description': 'Classic fit denim jeans.',
                'price': Decimal('79.99'),
                'compare_price': Decimal('119.99'),
                'sku': 'PDJ-001',
                'stock_quantity': 150,
                'is_featured': True,
                'featured_image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&q=80',
            },
            {
                'name': 'Cotton T-Shirt Pack',
                'category': clothing,
                'description': 'Pack of 3 premium cotton t-shirts.',
                'price': Decimal('29.99'),
                'compare_price': Decimal('44.99'),
                'sku': 'CTP-001',
                'stock_quantity': 200,
                'is_featured': False,
                'featured_image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80',
            },
            {
                'name': 'Winter Jacket',
                'category': clothing,
                'description': 'Warm and stylish winter jacket.',
                'price': Decimal('149.99'),
                'compare_price': Decimal('199.99'),
                'sku': 'WJ-001',
                'stock_quantity': 80,
                'is_featured': True,
                'featured_image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80',
            },
            {
                'name': 'Running Shoes',
                'category': clothing,
                'description': 'Comfortable running shoes.',
                'price': Decimal('89.99'),
                'compare_price': Decimal('119.99'),
                'sku': 'RS-001',
                'stock_quantity': 120,
                'is_featured': True,
                'featured_image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80',
            },
            {
                'name': 'Stainless Steel Coffee Maker',
                'category': home,
                'description': 'Premium coffee maker.',
                'price': Decimal('129.99'),
                'compare_price': Decimal('179.99'),
                'sku': 'SSCM-001',
                'stock_quantity': 45,
                'is_featured': True,
                'featured_image': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&q=80',
            },
            {
                'name': 'LED Desk Lamp',
                'category': home,
                'description': 'Adjustable LED desk lamp.',
                'price': Decimal('39.99'),
                'compare_price': Decimal('59.99'),
                'sku': 'LDL-001',
                'stock_quantity': 90,
                'is_featured': False,
                'featured_image': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&q=80',
            },
            {
                'name': 'Kitchen Knife Set',
                'category': home,
                'description': 'Professional kitchen knife set.',
                'price': Decimal('89.99'),
                'compare_price': Decimal('129.99'),
                'sku': 'KKS-001',
                'stock_quantity': 60,
                'is_featured': True,
                'featured_image': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=800&q=80',
            },
            {
                'name': 'Non-Stick Cookware Set',
                'category': home,
                'description': 'Complete non-stick cookware set.',
                'price': Decimal('199.99'),
                'compare_price': Decimal('279.99'),
                'sku': 'NSCS-001',
                'stock_quantity': 35,
                'is_featured': False,
                'featured_image': 'https://images.unsplash.com/photo-1556908153-619b8c9d8be4?w=800&q=80',
            },
            {
                'name': 'Python Programming Guide',
                'category': books,
                'description': 'Comprehensive Python programming guide.',
                'price': Decimal('49.99'),
                'compare_price': Decimal('69.99'),
                'sku': 'PPG-001',
                'stock_quantity': 100,
                'is_featured': True,
                'featured_image': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&q=80',
            },
            {
                'name': 'Web Development Masterclass',
                'category': books,
                'description': 'Learn modern web development.',
                'price': Decimal('44.99'),
                'compare_price': Decimal('59.99'),
                'sku': 'WDM-001',
                'stock_quantity': 85,
                'is_featured': False,
                'featured_image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&q=80',
            },
            {
                'name': 'Data Science Essentials',
                'category': books,
                'description': 'Practical data science handbook.',
                'price': Decimal('54.99'),
                'compare_price': Decimal('74.99'),
                'sku': 'DSE-001',
                'stock_quantity': 70,
                'is_featured': True,
                'featured_image': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=800&q=80',
            },
            {
                'name': 'Marketing Strategy Guide',
                'category': books,
                'description': 'Essential digital marketing strategies.',
                'price': Decimal('39.99'),
                'compare_price': Decimal('54.99'),
                'sku': 'MSG-001',
                'stock_quantity': 95,
                'is_featured': False,
                'featured_image': 'https://images.unsplash.com/photo-1533750204176-3b0d38e9ac2d?w=800&q=80',
            },
        ]

        created_count = 0
        updated_count = 0

        for product_data in products_data:
            try:
                product, created = Product.objects.update_or_create(
                    sku=product_data['sku'],
                    defaults=product_data
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Created: {product.name}'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Updated: {product.name}'))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error with {product_data["name"]}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Success! Created {created_count} new products, updated {updated_count} existing products'
            )
        )
