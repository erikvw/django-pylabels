from io import BytesIO
from typing import TYPE_CHECKING, Any

from pylabels import Sheet, Specification
from reportlab.pdfgen import canvas

from .get_label_specification import get_label_specification

if TYPE_CHECKING:
    from collections.abc import Callable

    from reportlab.graphics.shapes import Drawing


def blank_buffer() -> BytesIO:
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def save_to_buffer(
    objects: list,
    draw_label: Callable[[Drawing, int | float, int | float, Any], Drawing],
    label_specification: str | None = None,
) -> BytesIO:
    if len(objects) == 0:
        return blank_buffer()
    obj = get_label_specification(name=label_specification)
    specs = Specification(**obj.as_dict)
    sheet = Sheet(specs, draw_label, border=obj.border)
    sheet.add_labels(objects)
    return sheet.save_to_buffer()
