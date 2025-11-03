from django.urls import path
from . import views

urlpatterns = [
    path("rider/", views.rider_dashboard, name="rider dashboard"),
    path("driver/", views.driver_dashboard, name="driver dashboard"),
    path('moderator/', views.moderator_dashboard, name='moderator_dashboard'),
    path("create-post/", views.create_carpool_post, name="create_carpool_post"),
    path('flag-post/<int:post_id>/', views.flag_post, name='flag_post'),
    path("", views.landing, name="landing")
]
