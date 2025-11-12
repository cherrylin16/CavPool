from django.urls import path
from . import views

urlpatterns = [
    path("rider/", views.rider_dashboard, name="rider dashboard"),
    path("driver/", views.driver_dashboard, name="driver dashboard"),
    path('moderator/', views.moderator_dashboard, name='moderator_dashboard'),
    path('moderator/flagged-posts/', views.flagged_posts, name='flagged_posts'),
    path('moderator/user-analytics/', views.user_analytics, name='user_analytics'),
    path('moderator/moderate-post/<int:post_id>/', views.moderate_post, name='moderate_post'),
    path('moderator/ban-user/', views.ban_user, name='ban_user'),
    path("create-post/", views.create_carpool_post, name="create_carpool_post"),
    path('flag-post/<int:post_id>/', views.flag_post, name='flag_post'),
    path('submit-review/<int:post_id>/', views.submit_review, name='submit_review'),
    path("", views.landing, name="landing")
]
