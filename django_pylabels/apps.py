from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_pylabels"
    verbose_name = "Django pylabels"
    include_in_administration_section = True
