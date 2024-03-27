from django.contrib.auth.hashers import check_password
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from account.managers import CustomUserManager


class User(AbstractUser):
    phone = models.CharField(
        _('Phone Number'),
        max_length=10,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(
        _('First Name'),
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=150,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('Email Address'),
        max_length=250,
        blank=True,
        null=True
    )

    national_id = models.CharField(
        _('National ID'),
        max_length=10,
        null=True,
        blank=True
    )

    image = models.ImageField(verbose_name=_('image'),
                              upload_to='images/users',
                              blank=True, null=True
                              )

    password = models.CharField(
        _('password'),
        max_length=512,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False
    )

    username = None
    date_joined = None
    last_login = None
    groups = None
    user_permissions = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name:
            return f'{self.first_name}'
        elif self.last_name:
            return f'{self.last_name}'
        else:
            return f'{self.phone}'

    def save(self, *args, **kwargs):
        if self.password:
            self.set_password(self.password)

        super(User, self).save(*args, **kwargs)


class CardNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='card_numbers')
    card_number = models.CharField(
        _('Card Number'),
        max_length=16,
        unique=True,

    )

    sheba_number = models.CharField(
        _('Sheba Number'),
        max_length=24,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        _('active status'),
        default=False
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )

    class Meta:
        db_table = 'UserCardNumber'
        verbose_name = _('Card Number')
        verbose_name_plural = _('Card Numbers')

    def __str__(self):
        return f'{self.user.phone} - {self.card_number}'


class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    wallet_balance = models.DecimalField(
        _('Wallet Balance'),
        max_digits=8,
        decimal_places=3,
        default=0,
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )

    class Meta:
        db_table = 'user_wallet'
        verbose_name = _('User Wallet')
        verbose_name_plural = _('User Wallets')

    def __str__(self):
        return f'{self.user.phone}'
