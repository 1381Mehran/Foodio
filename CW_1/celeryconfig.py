import os


# CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
# CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
#
# CELERY_TIMEZONE = 'Asia/Tehran'
#
# USE_TZ = True

broker_url = os.environ.get('CELERY_BROKER_URL')
result_backend = os.environ.get('CELERY_RESULT_BACKEND')

timezone = 'Asia/Tehran'
