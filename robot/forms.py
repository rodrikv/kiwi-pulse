from django import forms
from .models import Robot

# write a form to hide the password characters

class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['username', 'password', 'settings']
        widgets = {
            'password': forms.PasswordInput(),
        }
