# Generated by Django 4.2.12 on 2024-05-24 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_id', models.CharField(max_length=30)),
                ('equipment_code', models.CharField(default=None, max_length=100)),
                ('equipment_name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20, unique=True)),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compname', models.CharField(max_length=100)),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('T_id', models.CharField(max_length=20)),
                ('T_type', models.CharField(choices=[('IN', 'IN'), ('OUT', 'OUT')], max_length=3)),
                ('T_date', models.DateField(default=django.utils.timezone.now)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorymanager.categories')),
                ('equipment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorymanager.assets')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorymanager.customuser')),
            ],
        ),
        migrations.AddField(
            model_name='assets',
            name='category_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorymanager.categories'),
        ),
        migrations.CreateModel(
            name='Allocated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_on', models.DateField(default=django.utils.timezone.now)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorymanager.categories')),
                ('equipment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorymanager.assets')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorymanager.customuser')),
            ],
        ),
    ]
