import threading

from django.conf import settings
from django.core.mail import send_mail

from extensions.loggers import logger_info, logger_error


class SendMailThread(threading.Thread):
    def __init__(self, subject: str, massage: str, receivers: list):
        self.subject = subject
        self.massage = massage
        self.receivers = receivers

        threading.Thread.__init__(self)

    def run(self) -> None:
        from_email = settings.EMAIL_HOST_USER

        logger_info.info(f'Sending {self.subject} to {list(self.receivers)}')

        try:
            send_mail(self.subject, self.massage, from_email, self.receivers, fail_silently=False)
        except Exception as e:
            logger_error.error(str(e))
            logger_error.error(locals())
        else:
            logger_info.info(f'Sent {self.subject} to {list(self.receivers)}')
