from django.urls import path
from . import views

urlpatterns = [
    path("rider/", views.rider_dashboard, name="rider dashboard"),
    path("driver/", views.driver_dashboard, name="driver dashboard"),
    path("create-post/", views.create_carpool_post, name="create_carpool_post"),
    path("", views.landing, name="landing")
]
