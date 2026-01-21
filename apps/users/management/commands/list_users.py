"""
Management command to list all users and their roles
Usage: python manage.py list_users
"""
from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = 'List all users and their permissions'

    def handle(self, *args, **options):
        users = User.objects.all().order_by('-date_joined')
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found in database'))
            return

        self.stdout.write(self.style.SUCCESS(f'\nFound {users.count()} users:\n'))
        self.stdout.write('-' * 100)
        
        header = f"{'Email':<40} {'Role':<10} {'Active':<8} {'Staff':<8} {'Superuser':<10} {'Joined'}"
        self.stdout.write(self.style.SUCCESS(header))
        self.stdout.write('-' * 100)

        for user in users:
            email = user.email[:37] + '...' if len(user.email) > 40 else user.email
            role_style = self.style.SUCCESS if user.role == 'admin' else self.style.WARNING
            
            row = f"{email:<40} {user.role:<10} "
            row += f"{'Yes' if user.is_active else 'No':<8} "
            row += f"{'Yes' if user.is_staff else 'No':<8} "
            row += f"{'Yes' if user.is_superuser else 'No':<10} "
            row += f"{user.date_joined.strftime('%Y-%m-%d')}"
            
            self.stdout.write(role_style(row))

        self.stdout.write('-' * 100)
        
        admin_count = users.filter(role='admin').count()
        self.stdout.write(self.style.SUCCESS(f'\nAdmin users: {admin_count}'))
        self.stdout.write(self.style.WARNING(f'Regular users: {users.count() - admin_count}\n'))
