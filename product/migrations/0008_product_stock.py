# Generated by Django 5.0.2 on 2024-05-22 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_remove_midcat_parent_remove_subcat_parent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0, verbose_name='stock'),
        ),
    ]