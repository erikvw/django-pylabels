import csv
import uuid
from pathlib import Path

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


def export_to_csv(modeladmin, request, queryset):
    filename = Path("~/").expanduser() / "label_specifications.csv"
    if queryset.count() > 0:
        fieldnames = [f.name for f in queryset.model._meta.get_fields()]
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for obj in queryset:
                writer.writerow({fname: getattr(obj, fname) for fname in fieldnames})
