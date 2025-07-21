import csv
import io
import uuid
from zoneinfo import ZoneInfo

from dateutil.utils import today
from django.contrib import messages
from django.http import FileResponse
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
    if queryset.count() > 0:
        fieldnames = [f.name for f in queryset.model._meta.get_fields()]
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=fieldnames)
        writer.writeheader()
        for obj in queryset:
            writer.writerow({fname: getattr(obj, fname) for fname in fieldnames})
        buffer.seek(0)
        formatted_now = today(tzinfo=ZoneInfo("UTC")).strftime("%Y-%m-%d %H:%M")
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f"label_specifications_{formatted_now}.csv",
        )
    return None
