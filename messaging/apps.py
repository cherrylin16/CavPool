from django.apps import AppConfig
import os

class MessagingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messaging"
    path = os.path.dirname(os.path.abspath(__file__))