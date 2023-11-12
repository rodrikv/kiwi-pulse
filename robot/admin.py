from django.contrib import admin
from .forms import RobotForm, MediaForm

from .models import Robot, Caption, Media, UserTag, Post


class RobotAdmin(admin.ModelAdmin):
    list_display = ("username",)

    form = RobotForm

    fieldsets = ((None, {"fields": ("username", "password", "settings")}),)


class MediaAdmin(admin.ModelAdmin):
    list_display = ("name", "media_type", "media_file")

    form = MediaForm

    fieldsets = ((None, {"fields": ("name", "media_file")}),)


class CaptionAdmin(admin.ModelAdmin):
    list_display = ("text",)

    fieldsets = ((None, {"fields": ("text",)}),)


admin.site.register(Robot, RobotAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Post)
admin.site.register(Caption)
admin.site.register(UserTag)
