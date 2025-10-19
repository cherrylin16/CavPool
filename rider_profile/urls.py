from django.urls import path
from . import views

urlpatterns = [
    path("rider_profile/",views.rider_profile),
]