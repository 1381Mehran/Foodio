from datetime import timedelta

from celery import shared_task

from extensions.loggers import logger_info


@shared_task
def check_seller_active(instance, created):
    if instance and created:
        if (instance.created_at + timedelta(minutes=1) and
           instance.is_active is False and instance.not_confirmed_cause is None):

            logger_info.info(f'seller with number {instance.user.phone} is not activated yet')
