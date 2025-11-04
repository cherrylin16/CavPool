from django.apps import AppConfig
import os

class DriverProfileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "driver_profile"
    path = os.path.dirname(os.path.abspath(__file__))