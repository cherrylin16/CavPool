from django.urls import path
from . import views

urlpatterns = [
    path("", views.messages_list, name="messages_list"),
    path("<str:username>/", views.message_detail, name="message_detail"),
]