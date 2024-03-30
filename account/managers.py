from django.contrib.auth.models import UserManager
from django.contrib.auth import get_user_model


class CustomUserManager(UserManager):
    def create_user(self, phone, email=None, password=None, **extra_fields):
        if not phone:
            raise ValueError('phone is required')

        user = get_user_model().objects.create(
            phone=phone,
            email=email,
            password=password
        )

        return user

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        user = self.create_user(
            phone=phone,
            email=email,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True

        user.save(update_fields=['is_staff', 'is_superuser'])

        return user
