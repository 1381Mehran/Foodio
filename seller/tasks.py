from datetime import timedelta

from celery import shared_task

from extensions.loggers import logger_info
from .models import Seller


@shared_task
def check_seller_active(pk):

    if pk:
        instance = Seller.objects.get(pk=pk)

        if (instance.created_at + timedelta(minutes=1) and
           instance.is_active is False and instance.not_confirmed_cause is None):

            logger_info.info(f'seller with number {instance.user.phone} is not activated yet')

# @shared_task
# def check_seller_active2(pk):
#
#     if pk:
#         instance = Seller.objects.get(pk=pk)
#
#         if (instance.created_at + timedelta(minutes=1) and
#            instance.is_active is False and instance.not_confirmed_cause is None):
#
#             logger_info.info(f'seller with number {instance.user.phone} is not activated yet')
