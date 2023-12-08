from celery import shared_task
from robot.models import Post, Story
from datetime import timedelta, datetime

from time import sleep
from typing import Optional


@shared_task
def check_media_to_publish():
    now = datetime.now()
    one_minute_later = now + timedelta(minutes=1)

    media_types = [
        Post,
        Story
    ]

    for media_type in media_types:
    # Filter posts scheduled to be published in the next one minute
        medias_to_publish = media_type.objects.filter(
            published=False,
            publish_at__lte=one_minute_later
        )
        # publish each post
        for post in medias_to_publish:
            post.publish()

            print("published post: ", post)

        # send notification to email


@shared_task
def send_notification():
    # send notification to email
    pass
