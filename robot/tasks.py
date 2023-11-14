from celery import shared_task
from robot.models import Post

@shared_task
def check_media_to_publish():
    # check if there is any media to publish in next one minute
    # if yes, publish it

    # get all posts that are scheduled to be published in next one minute
    posts = Post.objects.filter(published=False)

    # publish each post
    for post in posts:
        post.publish()

        print("published post: ", post)

        # send notification to email


@shared_task
def send_notification():
    # send notification to email
    pass
