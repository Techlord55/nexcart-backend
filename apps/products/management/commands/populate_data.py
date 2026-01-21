"""
Management command to populate sample data
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.products.models import Category, Product
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populates the database with sample products and categories'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Clear existing data
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Create Categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Latest gadgets and electronic devices',
            },
            {
                'name': 'Clothing',
                'description': 'Fashion and apparel for everyone',
            },
            {
                'name': 'Books',
                'description': 'Wide selection of books and literature',
            },
            {
                'name': 'Home & Kitchen',
                'description': 'Everything for your home',
            },
            {
                'name': 'Sports & Outdoors',
                'description': 'Sports equipment and outdoor gear',
            },
        ]

        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories[cat_data['name']] = category
            self.stdout.write(f'Created category: {category.name}')

        # Create Products
        products_data = [
            # Electronics
            {
                'name': 'Wireless Bluetooth Headphones',
                'category': 'Electronics',
                'price': Decimal('79.99'),
                'compare_price': Decimal('129.99'),
                'description': 'Premium wireless headphones with noise cancellation and 30-hour battery life.',
                'short_description': 'Premium wireless headphones with noise cancellation',
                'is_featured': True,
                'stock_quantity': 50,
            },
            {
                'name': 'Smart Watch Pro',
                'category': 'Electronics',
                'price': Decimal('299.99'),
                'compare_price': Decimal('399.99'),
                'description': 'Advanced fitness tracking, heart rate monitor, and smartphone notifications.',
                'short_description': 'Advanced fitness tracking smartwatch',
                'is_featured': True,
                'stock_quantity': 30,
            },
            {
                'name': 'USB-C Charging Cable 6ft',
                'category': 'Electronics',
                'price': Decimal('12.99'),
                'description': 'Fast charging USB-C cable with durable braided design.',
                'short_description': 'Fast charging USB-C cable',
                'is_featured': False,
                'stock_quantity': 200,
            },
            {
                'name': 'Portable Power Bank 20000mAh',
                'category': 'Electronics',
                'price': Decimal('45.99'),
                'compare_price': Decimal('59.99'),
                'description': 'High-capacity power bank with dual USB ports and fast charging.',
                'short_description': 'High-capacity portable power bank',
                'is_featured': False,
                'stock_quantity': 75,
            },
            # Clothing
            {
                'name': 'Classic Cotton T-Shirt',
                'category': 'Clothing',
                'price': Decimal('24.99'),
                'description': 'Comfortable 100% cotton t-shirt available in multiple colors.',
                'short_description': '100% cotton comfortable t-shirt',
                'is_featured': False,
                'stock_quantity': 150,
            },
            {
                'name': 'Denim Jeans - Slim Fit',
                'category': 'Clothing',
                'price': Decimal('59.99'),
                'compare_price': Decimal('89.99'),
                'description': 'Premium denim jeans with modern slim fit and stretch comfort.',
                'short_description': 'Premium slim fit denim jeans',
                'is_featured': True,
                'stock_quantity': 80,
            },
            {
                'name': 'Winter Puffer Jacket',
                'category': 'Clothing',
                'price': Decimal('129.99'),
                'compare_price': Decimal('199.99'),
                'description': 'Warm and stylish puffer jacket perfect for cold weather.',
                'short_description': 'Warm winter puffer jacket',
                'is_featured': True,
                'stock_quantity': 45,
            },
            # Books
            {
                'name': 'The Art of Programming',
                'category': 'Books',
                'price': Decimal('34.99'),
                'description': 'Comprehensive guide to modern programming techniques and best practices.',
                'short_description': 'Modern programming guide',
                'is_featured': False,
                'stock_quantity': 100,
            },
            {
                'name': 'Cooking Masterclass',
                'category': 'Books',
                'price': Decimal('29.99'),
                'compare_price': Decimal('44.99'),
                'description': 'Learn professional cooking techniques from world-class chefs.',
                'short_description': 'Professional cooking guide',
                'is_featured': False,
                'stock_quantity': 60,
            },
            {
                'name': 'Mystery Novel Collection',
                'category': 'Books',
                'price': Decimal('19.99'),
                'description': 'Thrilling collection of bestselling mystery novels.',
                'short_description': 'Bestselling mystery novels',
                'is_featured': True,
                'stock_quantity': 90,
            },
            # Home & Kitchen
            {
                'name': 'Stainless Steel Cookware Set',
                'category': 'Home & Kitchen',
                'price': Decimal('149.99'),
                'compare_price': Decimal('249.99'),
                'description': '10-piece professional cookware set with non-stick coating.',
                'short_description': '10-piece cookware set',
                'is_featured': True,
                'stock_quantity': 35,
            },
            {
                'name': 'Smart Coffee Maker',
                'category': 'Home & Kitchen',
                'price': Decimal('89.99'),
                'description': 'Programmable coffee maker with WiFi connectivity and app control.',
                'short_description': 'Smart programmable coffee maker',
                'is_featured': False,
                'stock_quantity': 55,
            },
            {
                'name': 'Organic Cotton Bed Sheets',
                'category': 'Home & Kitchen',
                'price': Decimal('69.99'),
                'compare_price': Decimal('99.99'),
                'description': 'Luxurious organic cotton sheets with 400 thread count.',
                'short_description': 'Luxurious organic cotton sheets',
                'is_featured': False,
                'stock_quantity': 70,
            },
            # Sports & Outdoors
            {
                'name': 'Yoga Mat Premium',
                'category': 'Sports & Outdoors',
                'price': Decimal('39.99'),
                'description': 'Extra thick yoga mat with non-slip surface and carrying strap.',
                'short_description': 'Extra thick non-slip yoga mat',
                'is_featured': False,
                'stock_quantity': 120,
            },
            {
                'name': 'Camping Tent 4-Person',
                'category': 'Sports & Outdoors',
                'price': Decimal('179.99'),
                'compare_price': Decimal('249.99'),
                'description': 'Waterproof camping tent with easy setup and ventilation.',
                'short_description': 'Waterproof 4-person camping tent',
                'is_featured': False,
                'stock_quantity': 25,
            },
        ]

        featured_count = 0
        for idx, prod_data in enumerate(products_data, 1):
            category_name = prod_data.pop('category')
            prod_data['category'] = categories[category_name]
            prod_data['sku'] = f'PROD-{idx:04d}'
            
            # Set random ratings
            prod_data['average_rating'] = Decimal(str(round(random.uniform(3.5, 5.0), 1)))
            prod_data['review_count'] = random.randint(10, 150)
            prod_data['view_count'] = random.randint(50, 500)
            prod_data['purchase_count'] = random.randint(5, 100)
            
            product = Product.objects.create(**prod_data)
            
            if product.is_featured:
                featured_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created product: {product.name} (Featured: {product.is_featured})'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {len(categories_data)} categories '
                f'and {len(products_data)} products ({featured_count} featured)'
            )
        )
