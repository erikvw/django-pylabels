# Generated by Django 5.1.2 on 2024-11-06 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_pylabels", "0003_rename_updated_labelspecification_modified"),
    ]

    operations = [
        migrations.AlterField(
            model_name="labelspecification",
            name="label_description",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="labelspecification",
            name="layout_description",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="labelspecification",
            name="page_description",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
