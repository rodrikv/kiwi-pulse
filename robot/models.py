from django.db import models
from instagrapi import Client
from django.utils.translation import gettext_lazy as _

from django.core.cache import cache


# Create your models here.
class Robot(models.Model):
    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    password = models.CharField(max_length=50, blank=False, null=False)
    settings = models.JSONField(default=dict, blank=True, null=True)
    client_timeout = 60 * 60 * 24 * 7

    def set_client(self, client: Client):
        cache.set(self.username, client, timeout=self.client_timeout)

    def get_client(self) -> Client:
        if not self.username:
            return Client()
        client = cache.get(self.username)
        if client is None:
            client = Client()
            is_set = client.set_settings(self.settings)
            if is_set:
                cache.set(self.username, client, timeout=self.client_timeout)
                return client
            client.login(self.username, self.password)
            cache.set(self.username, client, timeout=self.client_timeout)
        return client

    def get_logged_in_client(self) -> Client:
        client = self.get_client()
        client.login(self.username, self.password)
        return client

    # after the model is created, if settings is empty, it will be filled with default values
    def save(self, *args, **kwargs):
        if not self.settings:
            cl = Client()
            cl.login(self.username, self.password)
            self.settings = cl.get_settings()
            self.set_client(cl)
        super().save(*args, **kwargs)

    def publish_album(
        self,
        paths,
        caption: str,
        usertags=[],
        location=None,
        configure_timeout: int = 3,
        configure_handler=None,
        configure_exception=None,
        to_story: bool = False,
        custom_accessibility_caption: str = None,
        like_and_view_counts_disabled: int = None,
        disable_comments: int = None,
        invite_coauthor_user_id: int = None
    ):
            client = self.get_logged_in_client()

            extra_data = {}
            if custom_accessibility_caption is not None:
                extra_data["custom_accessibility_caption"] = custom_accessibility_caption

            if like_and_view_counts_disabled is not None:
                extra_data["like_and_view_counts_disabled"] = like_and_view_counts_disabled

            if disable_comments is not None:
                extra_data["disable_comments"] = disable_comments

            if invite_coauthor_user_id is not None:
                extra_data["invite_coauthor_user_id"] = invite_coauthor_user_id

            media = client.album_upload(
                paths,
                caption=caption,
                usertags=usertags,
                location=location,
                configure_timeout=configure_timeout,
                configure_handler=configure_handler,
                configure_exception=configure_exception,
                extra_data=extra_data
            )

            return media

    def publish_post(
        self,
        paths,
        caption: str,
        usertags=[],
        location=None,
        custom_accessibility_caption: str = None,
        like_and_view_counts_disabled: int = None,
        disable_comments: int = None,
        invite_coauthor_user_id: int = None
    ):
        client = self.get_logged_in_client()
        
        extra_data = {}
        if custom_accessibility_caption is not None:
            extra_data["custom_accessibility_caption"] = custom_accessibility_caption

        if like_and_view_counts_disabled is not None:
            extra_data["like_and_view_counts_disabled"] = like_and_view_counts_disabled

        if disable_comments is not None:
            extra_data["disable_comments"] = disable_comments

        if invite_coauthor_user_id is not None:
            extra_data["invite_coauthor_user_id"] = invite_coauthor_user_id


        media = client.photo_upload(
            paths,
            caption=caption,
            usertags=usertags,
            location=location,
            extra_data=extra_data
        )

        return media

    def publish_video(
        self,
        path,
        caption: str,
        thumbnail = None,
        usertags = [],
        location = None,
        custom_accessibility_caption: str = None,
        like_and_view_counts_disabled: int = None,
        disable_comments: int = None,
        invite_coauthor_user_id: int = None
    ):
        client = self.get_logged_in_client()

        extra_data = {}
        if custom_accessibility_caption is not None:
            extra_data["custom_accessibility_caption"] = custom_accessibility_caption

        if like_and_view_counts_disabled is not None:
            extra_data["like_and_view_counts_disabled"] = like_and_view_counts_disabled

        if disable_comments is not None:
            extra_data["disable_comments"] = disable_comments

        if invite_coauthor_user_id is not None:
            extra_data["invite_coauthor_user_id"] = invite_coauthor_user_id

        media = client.video_upload(
            path = path,
            caption = caption,
            thumbnail = thumbnail,
            usertags = usertags,
            location = location,
            extra_data = extra_data
        )

        return media

    def __str__(self):
        return self.username


class Media(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    media_file = models.FileField(upload_to="media/")

    media_type = models.CharField(
        max_length=10,
        choices=[
            ("photo", "Photo"),
            ("video", "Video"),
            ("audio", "Audio"),
        ],
    )

    def __str__(self):
        return self.name


class Caption(models.Model):
    name = models.CharField(max_length=50, unique=True)
    text = models.TextField(max_length=500, verbose_name="caption")

    def __str__(self):
        return self.name


class UserTag(models.Model):
    username = models.CharField(max_length=50, verbose_name="username", unique=True)

    def __str__(self):
        return "@" + self.username


class Post(models.Model):
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE)
    caption = models.ForeignKey(Caption, on_delete=models.DO_NOTHING)
    usertags = models.ManyToManyField(UserTag, blank=True)
    medias = models.ManyToManyField(Media, verbose_name="Post Medias")
    published = models.BooleanField(default=False)

    publish_at = models.DateTimeField(verbose_name="Post At")

    def publish(self):
        if self.published:
            return

        medias = [media for media in self.medias.all()]

        if len(medias) > 1:
            self.robot.publish_album(
                list(map(lambda x: x.media_file.path, medias)),
                self.caption.text
            )

        elif medias[0].media_type == "photo":
            self.robot.publish_post(
                medias[0].media_file.path,
                self.caption.text,
            )

        elif medias[0].media_type == "video":
            self.robot.publish_video(
                medias[0].media_file.path,
                self.caption.text,
            )

        self.published = True
        self.save()

    def __str__(self) -> str:
        return self.robot.username + " caption: " + self.caption.text[:20]
