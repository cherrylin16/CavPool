from django.urls import path
from . import views

urlpatterns = [
    path("driver_profile/",views.driver_profile),
]