# Generated by Django 5.0.2 on 2024-02-29 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
    ]
