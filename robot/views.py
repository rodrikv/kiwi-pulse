from django.http import JsonResponse
from .models import Robot

def get_robots(request):
    robots = Robot.objects.all()

    robot = robots[0]

    # return a json response
    return JsonResponse(robot.get_client().user_id, safe=False)
