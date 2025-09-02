from django.urls import path
from . import views

urlpatterns = [
    path("system-status/", views.system_status, name="system_status"),
]
