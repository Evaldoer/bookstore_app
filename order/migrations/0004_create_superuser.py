from django.db import migrations
from django.contrib.auth.models import User

def create_superuser(apps, schema_editor):
    if not User.objects.filter(username="evaldo").exists():
        User.objects.create_superuser(
            username="evaldo",
            email="evaldo.dev2025@gmail.com",
            password="admin123"
        )

class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_order_quantity'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]