# Generated by Django 4.1.1 on 2022-09-18 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("drug", "0007_rename_verifed_prescriptionitem_verified"),
    ]

    operations = [
        migrations.RemoveField(model_name="prescriptionitem", name="verified",),
    ]
