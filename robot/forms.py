from django import forms
from .models import Robot, Media

# write a form to hide the password characters

class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['username', 'password', 'settings']
        widgets = {
            'password': forms.PasswordInput(),
        }


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['name', 'media_file']

    # if media was a video or a photo, save it
    # if media was an audio, don't save it
    def save(self, commit=True):
        media = super().save(commit=False)
        # check if the media is a video or a photo
        if self.cleaned_data['media_file'].content_type.startswith('image'):
            media.media_type = 'photo'

        elif self.cleaned_data['media_file'].content_type.startswith('video'):
            media.media_type = 'video'

        elif self.cleaned_data['media_file'].content_type.startswith('audio'):
            media.media_type = 'audio'

        else:
            raise forms.ValidationError("Invalid media type")

        media.media_file = self.cleaned_data['media_file']
        if commit:
            media.save()
        return media