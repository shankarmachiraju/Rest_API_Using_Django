"""Api config file."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """API configuration class.

    Parameters
    ----------
    AppConfig : django.apps
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.api"
