from django.db import models
from instagrapi import Client, exceptions


# Create your models here.
class Robot(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    settings = models.JSONField(default=dict, blank=True, null=True)

    # after the model is created, if settings is empty, it will be filled with default values
    def save(self, *args, **kwargs):
        if not self.settings:
            cl = Client()
            try:
                cl.login(self.username, self.password)
            except exceptions.AuthException as e:
                # handle invalid credentials
                print(e)
            except exceptions.TwoFactorRequiredError:
                # handle 2FA
                print("2FA required")
            except exceptions.RequestError:
                # handle other errors
                print("Connection error")

            self.settings = cl.get_settings()
        super().save(*args, **kwargs)

    def get_client(self):
        cl = Client()
        cl.set_settings(self.settings)
        return cl

    def __str__(self):
        return self.username