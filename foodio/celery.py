import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodio.settings')

app = Celery('foodio')
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.task
def add(x, y): return


app.autodiscover_tasks()


