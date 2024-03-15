# Generated by Django 5.0.2 on 2024-03-12 17:06

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
            name='MidCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('main_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mid_cats', to='product.maincat', verbose_name='Mid Category')),
            ],
            options={
                'verbose_name': 'Mid Category',
                'verbose_name_plural': 'Mid Categories',
                'db_table': 'mid_categories',
            },
        ),
        migrations.CreateModel(
            name='SubCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('mid_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_cats', to='product.midcat', verbose_name='Sub Category')),
            ],
            options={
                'verbose_name': 'Sub Category',
                'verbose_name_plural': 'Sub Categories',
                'db_table': 'sub_categories',
            },
        ),
    ]
