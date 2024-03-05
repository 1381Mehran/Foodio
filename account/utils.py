from string import digits
from secrets import choice as secret_choice

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.contrib.auth.hashers import check_password

from rest_framework_simplejwt.tokens import RefreshToken


class Authentication:
    size = settings.OTP_SIZE
    otp_expiration = settings.OTP_EXPIRATION

    def otp_generator(self, size: int = size, char: str = digits) -> str:

        return "".join(secret_choice(char) for _ in range(size))

    def login(self, phone: str, password: str = None, *args, **kwargs) -> str:
        if password:
            try:
                user = get_user_model().objects.get(phone=phone)

                status = check_password(password, user.password)

                if status:

                    code = self.otp_generator()
                    cache.set(phone, code, settings.OTP_EXPIRATION * 60)

                    return code

                else:
                    return 'Invalid phone number or password'
            except get_user_model().DoesNotExist:
                return 'Invalid phone number or password'

        else:

            code = self.otp_generator()
            cache.set(phone, code, settings.OTP_EXPIRATION * 60)

            return code

    def verify(self, phone: int, code: int, *args, **kwargs):

        correct_code = cache.get(phone) if cache.get(phone) else None

        if correct_code:
            if code == correct_code:

                cache.delete(phone)

                user, status = get_user_model().objects.get_or_create(phone=phone)

                refresh = RefreshToken.for_user(user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status
            else:
                return 'code is invalid', False
        else:
            return 'OTP expired', False

    def logout(self, request):
        refresh_token = request.data.get('refresh')

        try:

            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()

            return 'You logged out successfully', True

        except Exception as e:
            return str(e.args[0]), False
