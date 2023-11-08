from django.urls import path
from . import views

urlpatterns = [
    path('robots/', views.get_robots, name='get_robots'),
]