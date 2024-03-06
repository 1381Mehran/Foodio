from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User

######################################################
#                    Models_schemas                  #
######################################################


class AdminSchema(models.Model):
    class AdminPosition(models.TextChoices):
        FINANCIAL = 'financial', _('Financial')
        TECHNICAL = 'technical', _('Technical')
        SUPPORT = 'support', _('Support')
        PRODUCT = 'product', _('Product')

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
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name=_('User'),
                                related_name='fodio_admin'
                                )

    class Meta:
        db_table = 'admin_section'
        verbose_name = _('Admin')
        verbose_name_plural = _('Admins')

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name}'
        elif self.user.first_name:
            return f'{self.user.first_name}'
        elif self.user.last_name:
            return f'{self.user.last_name}'
        else:
            return f'{self.user.phone}'


class Staff(AdminSchema):
    admin = models.ForeignKey(Admin,
                              on_delete=models.CASCADE,
                              related_name='admin_staff',
                              verbose_name=_('Admin User')
                              )

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name=_('User'),
                                related_name='fodio_staff'
                                )

    class Meta:
        db_table = 'staffs'
        verbose_name = _('staff')
        verbose_name_plural = _('staffs')

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name}'
        elif self.user.first_name:
            return f'{self.user.first_name}'
        elif self.user.last_name:
            return f'{self.user.last_name}'
        else:
            return f'{self.user.phone}'
