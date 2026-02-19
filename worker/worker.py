import os
from celery import Celery

celery = Celery("worker")
celery.conf.broker_url = os.getenv("REDIS_URL")
celery.conf.result_backend = os.getenv("REDIS_URL")
celery.autodiscover_tasks(["worker.tasks"])
