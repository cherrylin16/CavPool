from django.urls import path
from . import views

urlpatterns = [
    path("", views.messages_list, name="message_page"),
    path("chat/<int:user_id>/", views.chat_room, name="chat_room"),
    path("new/", views.new_message, name="new_message"),
]