# Generated by Django 4.1.1 on 2022-09-17 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("drug", "0004_rename_verified_prescription_labeled"),
    ]

    operations = [
        migrations.AddField(
            model_name="prescriptionitem",
            name="verifed",
            field=models.BooleanField(default=False),
        ),
    ]
