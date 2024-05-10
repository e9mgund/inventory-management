# Generated by Django 4.2.12 on 2024-05-10 07:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventorymanager', '0003_remove_assets_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='assets',
            name='assigned_on',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='assets',
            name='employee',
            field=models.CharField(default='Not Assigned', max_length=30),
        ),
        migrations.AlterField(
            model_name='assets',
            name='category',
            field=models.CharField(max_length=30),
        ),
        migrations.CreateModel(
            name='Assets1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_id', models.CharField(max_length=30)),
                ('equipment_name', models.CharField(max_length=30)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorymanager.assettype')),
            ],
        ),
    ]
