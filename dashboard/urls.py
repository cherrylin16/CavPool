from django.urls import path
from . import views

urlpatterns = [
    path("rider/", views.rider_dashboard, name="rider dashboard"),
    path("driver/", views.driver_dashboard, name="driver dashboard"),
    path("", views.landing, name="landing")
]
