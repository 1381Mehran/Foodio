from typing import Any

from django.conf import settings

from kavenegar import *


def send_sms(receptor: str, token: str) -> Any:
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        params = {
            'receptor': receptor,
            'template': 'verify',
            'token': token,
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)