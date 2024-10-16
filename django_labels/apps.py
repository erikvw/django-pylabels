from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_labels"
    verbose_name = "Django Labels"
    include_in_administration_section = True
