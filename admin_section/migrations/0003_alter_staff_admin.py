# Generated by Django 5.0.2 on 2024-03-04 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_section', '0002_alter_admin_national_id_alter_admin_sheba_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='admin_section.admin', verbose_name='admin_section'),
        ),
    ]
