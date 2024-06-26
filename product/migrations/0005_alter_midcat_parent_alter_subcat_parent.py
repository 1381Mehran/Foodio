# Generated by Django 5.0.2 on 2024-05-14 21:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_maincat_is_active_alter_midcat_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='midcat',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mid_cats', to='product.maincat', verbose_name='Main Category'),
        ),
        migrations.AlterField(
            model_name='subcat',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_cats', to='product.midcat', verbose_name='Mid Category'),
        ),
    ]
