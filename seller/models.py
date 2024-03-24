from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User


class State(models.Model):
    class Types(models.TextChoices):
        STATE = 'state', 'State'
        CITY = 'city', 'City'

    type = models.CharField(
        _('type'),
        max_length=5,
        choices=Types.choices,
        default=None
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name=_('parent'),
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=30,
        verbose_name=_('title')
    )

    is_active = models.BooleanField(_('is active'), default=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        db_table = 'states'
        verbose_name = _('state')
        verbose_name_plural = _('states')


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

    work_class_number = models.CharField(
        _('Work Class Number'),
        max_length=30
    )

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name='sellers',
        verbose_name=(_('states'))
    )

    address = models.CharField(
        _('Address'),
        max_length=300,
        help_text=_('Enter your work address')
    )

    is_active = models.BooleanField(_('is active'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        db_table = 'Sellers'
        verbose_name = _('Seller')
        verbose_name_plural = _('Sellers')
