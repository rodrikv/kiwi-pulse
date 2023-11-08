from django.shortcuts import HttpResponse
from .models import Robot

def get_robots(request):
    robots = Robot.objects.all()

    robot = robots[0]
    # return a json response
    return HttpResponse(
        str(robot.get_client().user_info_by_username(robot.username).dict())
    )
