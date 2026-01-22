"""
Update Product model to support both file uploads and external URLs for images
"""
from django.db import models, migrations


def update_image_fields(apps, schema_editor):
    """
    Convert ImageField to URLField to support external URLs
    """
    pass  # Data migration if needed


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),  # Replace with your latest migration
    ]

    operations = [
        # Change featured_image to URLField to store external URLs
        migrations.AlterField(
            model_name='product',
            name='featured_image',
            field=models.URLField(max_length=500, blank=True, null=True),
        ),
    ]
