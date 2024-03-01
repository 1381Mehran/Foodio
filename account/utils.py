from string import digits
from secrets import choice as secret_choice

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework_simplejwt.tokens import RefreshToken


class Authentication:
    size = settings.OTP_SIZE
    otp_expiration = settings.OTP_EXPIRATION

    def otp_generator(self, size: int = size, char: str = digits) -> str:
        return ''.join(secret_choice(char) for _ in range(size))

    def login(self, phone: str, password: str = None, *args, **kwargs):
        if password:
            try:
                user = get_user_model().objects.get(phone=phone)

                status = user.check_password(password)

                if status:

                    code = self.otp_generator()
                    cache.set(phone, code, settings.OTP_EXPIRATION * 60)

                    return int(code)

                else:
                    return 'Wrong password'

            except get_user_model().DoesNotExist:
                return 'Invalid phone number'

        else:

            code = self.otp_generator()
            cache.set(phone, code, settings.OTP_EXPIRATION * 60)

            return int(code)

    def verify(self, phone: int, code: int, *args, **kwargs):

        correct_code = int(cache.get(phone))

        if correct_code:
            if code == correct_code:
                user = get_user_model().objects.get(phone=phone)
                refresh = RefreshToken.for_user(user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            else:
                return 'code is invalid'
        else:
            return 'OTP expired'
