# Generated by Django 5.0.2 on 2024-03-27 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0004_state_parent_state_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='not_confirmed_cause',
            field=models.TextField(blank=True, null=True, verbose_name='not_confirmed_cause'),
        ),
    ]