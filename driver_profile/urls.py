from django.urls import path
from . import views

urlpatterns = [
    path("driver/profile/",views.driver_profile, name="driver_profile"),
]