
from django.urls import path
from . import views

urlpatterns = [
    path("rider/profile/",views.rider_profile, name="rider_profile"),
]