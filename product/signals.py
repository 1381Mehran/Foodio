from datetime import timedelta

from django.dispatch import receiver
from django.db.models.signals import post_save

from product.models import Product
from .tasks import product_check_active


@receiver(post_save, sender=Product)
def product_active_checker(sender, instance, created, **kwargs):
    if created:
        product_check_active.apply_async(args=[instance.pk], eta=instance.create_at + timedelta(minutes=1))
