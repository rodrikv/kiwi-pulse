from instagrapi import Client
from instagrapi.types import Usertag
from pathlib import Path

client = Client()

client.load_settings("settings.json")

client.login("asghar_asghari_8585", "yehaftedohafte")

user = client.user_info_by_username("txunao")

print(client.album_upload([
    Path("media/500.jpg"),
    Path("media/1.mp4")
],
caption="",
usertags=[
    Usertag(user=user, x=0.5, y=0.5)
]))