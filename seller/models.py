from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User


class State(models.Model):
    class Types(models.TextChoices):
        STATE = 'state', 'State'
        CITY = 'city', 'City'

    title = models.CharField(
        max_length=30,
        verbose_name=_('title')
    )

    is_active = models.BooleanField(_('is active'), default=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)


class Seller(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seller',
        verbose_name=_('User')
    )

    work_class = models.CharField(
        _('Work Class'),
        max_length=250
    )

    address = models.CharField(_('Address'), max_length=300)

