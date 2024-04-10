from datetime import timedelta

from django.utils import timezone

from celery import shared_task

from .models import Product
from extensions.loggers import logger_info


@shared_task
def product_check_active(pk):
    instance = Product.objects.get(pk=pk)

    if not instance.is_active and (instance.created_at + timedelta(minutes=30) < timezone.now()):
        logger_info.info('Product {0} is not active'.format(instance.title))


