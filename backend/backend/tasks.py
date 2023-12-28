from celery import Celery

celery = Celery('tasks', broker='pyamqp://guest:guest@redis:5672//')

@celery.task
def add(x, y):
    return x + y