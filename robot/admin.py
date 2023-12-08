from django.contrib import admin
from django.utils.html import format_html
from .forms import RobotForm, MediaForm, StoryForm

from .models import Robot, Caption, Media, UserTag, Post, Story


class RobotAdmin(admin.ModelAdmin):
    list_display = ("username",)

    form = RobotForm

    fieldsets = ((None, {"fields": ("username", "password", "settings", "test_robot")}),)


class MediaAdmin(admin.ModelAdmin):
    list_display = ("name", "media_type", "media_file")

    form = MediaForm

    def image_preview(self, obj):
        # Change 'image_field' to the actual name of your image field
        if obj.media_file:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.media_file.url)
        return '-'



    fieldsets = ((None, {"fields": ("name", "media_file")}),)


class CaptionAdmin(admin.ModelAdmin):
    list_display = ("text",)

    fieldsets = ((None, {"fields": ("text",)}),)


class StoryAdmin(admin.ModelAdmin):
    form = StoryForm


admin.site.register(Robot, RobotAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Post)
admin.site.register(Caption)
admin.site.register(UserTag)
