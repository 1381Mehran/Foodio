import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodio.settings')

app = Celery('foodio')

app.conf.update(
    broker_connection_retry_on_startup=True
)
#
# app.conf.task_routes = {
#     'seller.tasks.check_seller_active': {'queue': 'queue1'},
#     'seller.tasks.check_seller_active2': {'queue': 'queue2'},
# }

app.config_from_object('django.conf:settings', namespace='CELERY')

task_routes = ([
    ('seller.tasks.*', {'queue': 'seller'}),
    ('product.tasks.*', {'queue': 'product'}),
])


@app.task
def add(x, y): return


app.autodiscover_tasks()


