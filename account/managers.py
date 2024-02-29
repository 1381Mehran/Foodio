from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_user(self, phone, email=None, password=None, **extra_fields):
        if not phone:
            raise ValueError('phone is required')

        user = self.model(phone=phone)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        user = self.create_user(
            phone=phone,
            email=email,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user
