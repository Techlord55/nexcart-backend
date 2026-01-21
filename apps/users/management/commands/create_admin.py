"""
Management command to create an admin user
Usage: python manage.py create_admin
"""
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from apps.users.models import User, UserProfile


class Command(BaseCommand):
    help = 'Create an admin user'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Admin email address')
        parser.add_argument('--password', type=str, help='Admin password')
        parser.add_argument('--first-name', type=str, default='Admin', help='First name')
        parser.add_argument('--last-name', type=str, default='User', help='Last name')

    def handle(self, *args, **options):
        email = options.get('email')
        password = options.get('password')
        first_name = options.get('first_name') or 'Admin'
        last_name = options.get('last_name') or 'User'

        # Prompt for email if not provided
        if not email:
            email = input('Enter admin email: ')

        # Prompt for password if not provided
        if not password:
            import getpass
            password = getpass.getpass('Enter admin password: ')
            password_confirm = getpass.getpass('Confirm admin password: ')
            
            if password != password_confirm:
                self.stdout.write(self.style.ERROR('Passwords do not match!'))
                return

        try:
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f'User with email {email} already exists!'))
                
                # Ask if we should update to admin
                update = input('Update this user to admin? (y/n): ')
                if update.lower() == 'y':
                    user = User.objects.get(email=email)
                    user.role = 'admin'
                    user.is_staff = True
                    user.is_superuser = True
                    user.is_active = True
                    user.save()
                    
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated {email} to admin!'))
                return

            # Create new admin user
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='admin',
                is_staff=True,
                is_superuser=True,
                is_active=True,
                is_verified=True
            )

            # Create profile
            UserProfile.objects.create(user=user)

            self.stdout.write(self.style.SUCCESS(
                f'Successfully created admin user: {email}'
            ))
            self.stdout.write(self.style.SUCCESS(
                f'Name: {first_name} {last_name}'
            ))
            self.stdout.write(self.style.SUCCESS(
                'You can now login with these credentials!'
            ))

        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Error creating admin: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))
