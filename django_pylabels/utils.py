from __future__ import annotations

from typing import Callable

from django.contrib import messages
from django.http import FileResponse
from django.utils.translation import gettext as _
from pylabels import Sheet, Specification


def print_test_label_sheet(request, queryset, drawing_func: Callable, label_data_cls):
    """Function to call within a Django admin action.

    label_data_cls is any class with the attributes needed by the drawing_func

    For example:
        def print_test_label_sheet(modeladmin, request, queryset):
            return print_test_label_sheet(
                request, queryset, drawing_func: Callable, label_data_cls)
    """
    if queryset.count() > 1 or queryset.count() == 0:
        messages.add_message(
            request,
            messages.ERROR,
            _("Select one and only one existing label specification"),
        )
    else:
        obj = queryset.first()
        specs = Specification(**obj.as_dict)
        sheet = Sheet(specs, drawing_func, border=obj.border)
        sheet.add_labels([label_data_cls() for i in range(0, obj.rows * obj.columns)])
        buffer = sheet.save_to_buffer()

        return FileResponse(buffer, as_attachment=True, filename=f"test_print_{obj.name}.pdf")
