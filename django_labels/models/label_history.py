from django.db import models


class LabelHistory(models.Model):
    """A model to track printed labels"""

    reference = models.CharField(max_length=10, help_text="Label reference")
    object_reference = models.CharField(max_length=100, help_text="Object reference")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference
