# Generated by Django 5.0.2 on 2024-04-09 23:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial_base'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maincat',
            name='active',
        ),
        migrations.RemoveField(
            model_name='midcat',
            name='active',
        ),
        migrations.RemoveField(
            model_name='subcat',
            name='active',
        ),
        migrations.AddField(
            model_name='maincat',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AddField(
            model_name='midcat',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL, verbose_name='User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcat',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
    ]
