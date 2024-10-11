import uuid

from django.contrib import messages
from django.utils.translation import gettext as _


def copy_label_specification(modeladmin, request, queryset):
    if queryset.count() > 1 or queryset.count() == 0:
        messages.add_message(
            request,
            messages.ERROR,
            _("Select one and only one existing label specification"),
        )
    else:
        obj = queryset.first()
        obj.pk = None
        obj.name = uuid.uuid4()
        obj.save()
