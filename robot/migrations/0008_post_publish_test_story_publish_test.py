# Generated by Django 4.2.7 on 2023-11-25 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0007_alter_caption_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='publish_test',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='story',
            name='publish_test',
            field=models.BooleanField(default=True),
        ),
    ]
