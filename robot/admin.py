from django.contrib import admin
from .forms import RobotForm

from .models import Robot



class RobotAdmin(admin.ModelAdmin):
    list_display = ('username', )

    form = RobotForm

    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'settings')
        }),
    )


admin.site.register(Robot, RobotAdmin)
