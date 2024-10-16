from datetime import datetime
from typing import Any, Type
from zoneinfo import ZoneInfo

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model
from django.http import FileResponse
from django.utils.translation import gettext as _
from reportlab.graphics.shapes import Drawing

from .save_to_buffer import save_to_buffer


class PrintLabelsViewMixin:

    label_data_model: str = ""
    label_filename_prefix: str = _("labels")

    def get(self, request: WSGIRequest, *args, **kwargs) -> FileResponse:
        max_labels: int = int(request.GET.get("max_labels"))
        label_specification: str | None = request.GET.get("label_specification")
        objects = self.get_label_data(request, max_labels=max_labels)
        buffer = save_to_buffer(
            objects, self.draw_label, label_specification=label_specification
        )
        self.update_label_history(objects)
        return FileResponse(
            buffer, as_attachment=True, filename=self.get_label_filename(request)
        )

    def draw_label(
        self,
        label: Drawing,
        width: int | float,
        height: int | float,
        label_data_item: Any,
    ) -> Drawing:
        """See example in pylabels django demo"""
        raise ImproperlyConfigured()

    def get_label_data(
        self,
        request: WSGIRequest,
        max_labels: int = None,
    ) -> list:
        """See example in pylabels django demo"""
        raise ImproperlyConfigured()

    def get_label_filename(self, request: WSGIRequest) -> str:
        timestamp = (
            datetime.now().astimezone(ZoneInfo(settings.TIME_ZONE)).strftime("%Y%m%d%H%M%S")
        )
        return request.GET.get("filename") or f"{self.label_filename_prefix}_{timestamp}.pdf"

    def update_label_history(self, objects: list) -> None:
        pass

    def label_history_model_cls(self) -> Type[Model]:
        return django_apps.get_model(self.label_data_model)
