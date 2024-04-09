import os


# CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
# CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
#
# CELERY_TIMEZONE = 'Asia/Tehran'
#
# USE_TZ = True

broker_url = os.environ.get('CELERY_BROKER_URL')
result_backend = os.environ.get('CELERY_RESULT_BACKEND')

broker_connection_retry_on_startup = True

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Tehran'



