# Generated by Django 5.0.2 on 2024-03-17 20:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'Main Category',
                'verbose_name_plural': 'Main Categories',
                'db_table': 'main_categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=450, verbose_name='title')),
                ('introduce', models.TextField(blank=True, null=True, verbose_name='introduce')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'Products',
            },
        ),
        migrations.CreateModel(
            name='MidCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mid_cats', to='product.maincat', verbose_name='Mid Category')),
            ],
            options={
                'verbose_name': 'Mid Category',
                'verbose_name_plural': 'Mid Categories',
                'db_table': 'mid_categories',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/product', verbose_name='image')),
                ('type', models.CharField(choices=[('banner', 'Banner'), ('sub', 'Sub')], default='sub', max_length=6, verbose_name='type')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='product.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'db_table': 'product_images',
            },
        ),
        migrations.CreateModel(
            name='ProductProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('property', 'Property'), ('specification', 'Specification')], max_length=14, verbose_name='item type')),
                ('item_name', models.CharField(max_length=50, verbose_name='item name')),
                ('item_detail', models.CharField(max_length=300, verbose_name='item detail')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_properties', to='product.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Product property',
                'verbose_name_plural': 'Product properties',
                'db_table': 'Product_properties',
            },
        ),
        migrations.CreateModel(
            name='SubCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_cats', to='product.midcat', verbose_name='Sub Category')),
            ],
            options={
                'verbose_name': 'Sub Category',
                'verbose_name_plural': 'Sub Categories',
                'db_table': 'sub_categories',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_categories', to='product.subcat', verbose_name='Sub Category'),
        ),
    ]