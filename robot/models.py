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

    # after the model is created, if settings is empty, it will be filled with default values
    def save(self, *args, **kwargs):
        if not self.settings:
            cl = Client()
            cl.login(self.username, self.password)
            self.settings = cl.get_settings()

            self.set_client(cl)

        super().save(*args, **kwargs)

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

    publish_at = models.DateTimeField(verbose_name="Post At")

    def __str__(self) -> str:
        return self.robot.username + " caption: " + self.caption.text[:20]
