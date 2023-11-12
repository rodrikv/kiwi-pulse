# yourapp/tasks.py
from celery import shared_task

@shared_task
def your_periodic_task():
    print("hello world")
