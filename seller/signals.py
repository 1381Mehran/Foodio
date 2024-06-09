from datetime import timedelta

from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Seller
from .tasks import check_seller_active


@receiver(post_save, sender=Seller)
def seller_active_checker(sender, instance, created, **kwargs):

    if created:

        task = check_seller_active.apply_async(
            args=(instance.id,),
            eta=instance.created_at + timedelta(minutes=30),
            queue='seller'
        )

        instance.celery_task_id = task.id
        instance.save(update_fields=['celery_task_id'])
