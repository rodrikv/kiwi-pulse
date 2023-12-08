from django import forms
from instagrapi import Client

from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO


from .models import Robot, Media, UserTag, Story
from django.utils.translation import gettext_lazy as _

# write a form to hide the password characters


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ["username", "password", "settings", "test_robot"]
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

        if content_type.startswith("image"):
            if content_type == "image/png":
                # Convert PNG to JPG
                img = Image.open(media.media_file)
                if img.mode in ('RGBA', 'LA'):
                    img = img.convert('RGB')

                # Create a temporary BytesIO object to hold the converted image
                buffer = BytesIO()
                img.save(buffer, format='JPEG')
                buffer.seek(0)

                # Set the file name with .jpg extension
                file_name = f"{media.name}.jpg"  # Replace with your preferred file name

                # Save the BytesIO object to the model's media_file field using Django's ContentFile
                media.media_file.save(file_name, ContentFile(buffer.read()), save=False)

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


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

    def save_m2m(self):
        super().save_m2m()
        self.instance.pre_publish()