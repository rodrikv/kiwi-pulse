# yourapp/tasks.py
from celery import shared_task
from robot.models import Post

@shared_task
def check_media_to_publish():
    print(Post.object.all())
