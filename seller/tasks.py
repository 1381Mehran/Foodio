from datetime import timedelta

from celery import shared_task

from extensions.loggers import logger_info
from extensions.send_mail import SendMailThread
from .models import Seller
from admin_section.models import Admin


@shared_task
def check_seller_active(pk):

    if pk:
        instance = Seller.objects.get(pk=pk)

        if (instance.created_at + timedelta(minutes=30) and
           instance.is_active is False and instance.not_confirmed_cause is None):

            logger_info.info(f'seller with number {instance.user.phone} is not activated yet')

            product_admin_emails = Admin.objects.filter(
                position='product',
                is_active=True
            ).values_list('user__email', flat=True)

            SendMailThread(
                'فروشنده بدون تعیین وضعیت',
                f' فروشنده ای با شماره ی 0{instance.user.phone} و نام و نام خانوادگی {instance.user.first_name} {instance.user.last_name} هنوز بعد از گذشت 30 دقیقه تعیین وضعیت نشده است لطفا پیگیری نمایید با تشکر ',
                product_admin_emails
            ).start()


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
