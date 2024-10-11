from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from models import LabelSpecification


def get_label_specification(name: str | None) -> LabelSpecification:
    name = name or "default"
    try:
        obj = LabelSpecification.objects.get(name=name)
    except ObjectDoesNotExist:
        if name == "default":
            obj = LabelSpecification.objects.create(name=name)
        else:
            raise ObjectDoesNotExist(
                _(
                    "Label specification does not exist. "
                    f"Go to admin to create one or use 'default'. Got '{name}'."
                )
            )
    return obj
