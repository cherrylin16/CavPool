from django.urls import path
from . import views

urlpatterns = [
    path("", views.message_list, name="message_list"),
    path("new/", views.new_message, name="new_message"),
    path("<int:user_id>/", views.message_detail, name="message_detail"),
]