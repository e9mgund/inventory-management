# Generated by Django 4.2.12 on 2024-05-10 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventorymanager', '0002_assets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assets',
            name='quantity',
        ),
    ]