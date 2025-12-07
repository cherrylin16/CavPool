from django.urls import path
from . import views
from .views import view_driver_profile

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
    path('moderator/edit-post/<int:post_id>/', views.edit_carpool_post, name='edit_carpool_post'),
    path('edit-post/<int:post_id>/', views.edit_own_carpool_post, name='edit_own_carpool_post'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('submit-review/<int:post_id>/', views.submit_review, name='submit_review'),
    path('get-driver-info/<int:user_id>/', views.get_driver_info, name='get_driver_info'),
    path("landing/", views.landing, name="landing"),
    path("driver/<int:driver_id>/info/", view_driver_profile, name="view_driver_info"),

]
