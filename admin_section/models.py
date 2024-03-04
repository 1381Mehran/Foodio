from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


######################################################
#                    Models_schemas                  #
######################################################


class AdminSchema(models.Model):
    class AdminPosition(models.TextChoices):
        FINANCIAL = 'financial', _('Financial')
        TECHNICAL = 'technical', _('Technical')
        SUPPORT = 'support', _('Support')
        PRODUCT = 'product', _('Product')

    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                verbose_name=_('User')
                                )

    national_id = models.CharField(
        _('National ID'),
        max_length=10
    )

    sheba_number = models.CharField(
        _('Sheba Number'),
        max_length=24
    )

    image = models.ImageField(verbose_name=_('image'),
                              upload_to='images/admins/%Y/%m/%d/',
                              blank=True, null=True
                              )

    position = models.CharField(_('Position'),
                                max_length=10,
                                choices=AdminPosition,
                                default=AdminPosition.FINANCIAL
                                )

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        abstract = True


######################################################
#                       END                          #
######################################################


class Admin(AdminSchema):

    class Meta:
        db_table = 'admin_section'
        verbose_name = _('Admin')
        verbose_name_plural = _('Admins')


class Staff(AdminSchema):
    admin = models.ForeignKey(Admin,
                              on_delete=models.CASCADE,
                              related_name='staffs',
                              verbose_name=_('admin_section')
                              )

    class Meta:
        db_table = 'staffs'
        verbose_name = _('staff')
        verbose_name_plural = _('staffs')
