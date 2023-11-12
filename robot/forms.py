from django import forms
from instagrapi import Client

from .models import Robot, Media, UserTag
from django.utils.translation import gettext_lazy as _

# write a form to hide the password characters


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ["username", "password", "settings"]
        widgets = {
            "password": forms.PasswordInput(),
        }


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ["name", "media_file"]

    def clean(self):
        cleaned_data = super().clean()

        media_file = cleaned_data.get("media_file")
        if media_file:
            content_type = media_file.content_type

            if (
                not content_type.startswith("image")
                and not content_type.startswith("video")
                and not content_type.startswith("audio")
            ):
                self.add_error(
                    "media_file",
                    "Invalid media type. Supported types are image, video, and audio.",
                )

    def save(self, commit=True):
        media = super().save(commit=False)

        content_type = self.cleaned_data["media_file"].content_type

        # check if the media is a video or a photo
        if content_type.startswith("image"):
            media.media_type = "photo"

        elif content_type.startswith("video"):
            media.media_type = "video"

        elif content_type.startswith("audio"):
            media.media_type = "audio"

        if commit:
            media.save()
        return media

class UserTagForm(forms.ModelForm):
    class Meta:
        model = UserTag
        fields = ["username"]

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        if username:
            cl = Client()