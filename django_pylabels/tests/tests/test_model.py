import random
import string

from django.contrib.auth.models import User
from django.contrib.messages import MessageFailure
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse
from reportlab.graphics.shapes import Group, String
from reportlab.lib import colors

from django_pylabels.actions import copy_label_specification, export_to_csv
from django_pylabels.get_label_specification import get_label_specification
from django_pylabels.models import LabelSpecification
from django_pylabels.utils import print_test_label_sheet


class TestModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="erik")

    def setUp(self):
        self.user = User.objects.get(username="erik")

    def test_label_specification(self):
        self.assertEqual(LabelSpecification.objects.all().count(), 0)
        obj = get_label_specification("default")

        self.assertEqual(str(obj), "default")

        self.assertEqual(type(obj.as_dict), dict)

        self.assertEqual(obj.name, "default")
        self.assertEqual(obj.page_description, "210.0 x 297.0")
        self.assertEqual(obj.layout_description, "6 rows x 2 cols")
        self.assertEqual(obj.label_description, "96.0 x 42.0")

        obj = get_label_specification("default")
        self.assertEqual(obj.name, "default")
        self.assertEqual(obj.page_description, "210.0 x 297.0")
        self.assertEqual(obj.layout_description, "6 rows x 2 cols")
        self.assertEqual(obj.label_description, "96.0 x 42.0")

        self.assertRaises(ObjectDoesNotExist, get_label_specification, "blah")

        url = reverse("admin:django_pylabels_labelspecification_changelist")
        response = self.client.get(url)
        copy_label_specification(
            None, response.request, LabelSpecification.objects.all()
        )

        self.assertRaises(ObjectDoesNotExist, get_label_specification, "blah")

        obj = LabelSpecification.objects.exclude(pk=obj.pk)
        obj = get_label_specification(obj[0].name)
        self.assertEqual(obj.page_description, "210.0 x 297.0")
        self.assertEqual(obj.layout_description, "6 rows x 2 cols")
        self.assertEqual(obj.label_description, "96.0 x 42.0")

        factory = RequestFactory()
        request = factory.get(url)
        qs = LabelSpecification.objects.all()
        self.assertEqual(len(qs), 2)
        # assert it tries to add a message because the user selected more than
        # one model instance
        self.assertRaises(MessageFailure, copy_label_specification, None, request, qs)

        response = export_to_csv(
            None, response.request, LabelSpecification.objects.all()
        )
        self.assertEqual(type(response), FileResponse)
        self.assertTrue(
            response.filename.startswith("label_specification")
            and response.filename.endswith("csv")
        )

        class LabelData:

            def __init__(self):
                self.gender = random.choice(["M", "F"])  # nosec B311
                self.subject_identifier = "999-99-9999-9"  # nosec B311
                self.reference = "".join(
                    random.choices(
                        string.ascii_letters.upper() + "23456789", k=6
                    )  # nosec B311
                )
                self.sid = "12345"
                self.site_name = "AMANA"
                self.pills_per_bottle = 128

        def draw_label_watermark(label, width, height, *args, **string_options):
            string_opts = dict(
                fontName="Helvetica",
                fontSize=28,
                textAnchor="middle",
                fillColor=colors.Color(0.5, 0.5, 0.5, alpha=0.7),
            )
            string_opts.update(string_options)
            text_group = Group()
            watermark = String(height / 2, 10, "test label", **string_opts)
            text_group.add(watermark)
            text_group.translate(width / 3, height - height * 0.95)
            text_group.rotate(45)
            label.add(text_group)

        response = print_test_label_sheet(
            request,
            LabelSpecification.objects.filter(name="default"),
            draw_label_watermark,
            LabelData,
        )
        self.assertEqual(type(response), FileResponse)
