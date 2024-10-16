from django.contrib import admin

from .actions import copy_label_specification, export_to_csv
from .models import LabelHistory, LabelSpecification


@admin.register(LabelHistory)
class LabelHistoryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "object_reference", "created")
    list_filter = ("created",)
    search_fields = ("object_reference", "reference")


@admin.register(LabelSpecification)
class LabelSpecificationAdmin(admin.ModelAdmin):

    actions = [copy_label_specification, export_to_csv]

    list_display = (
        "name",
        "page_description",
        "layout_description",
        "label_description",
        "border",
    )

    readonly_fields = (
        "page_description",
        "layout_description",
        "label_description",
    )
