from celery_worker import celery_app
import time

@celery_app.task(name="tasks.add_numbers")
def add_numbers(a, b):
    time.sleep(5)
    return a + b
