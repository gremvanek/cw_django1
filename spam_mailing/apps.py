# apps.py
from django.apps import AppConfig


class SpamMailingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "spam_mailing"
