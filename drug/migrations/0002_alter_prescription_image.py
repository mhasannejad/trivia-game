# Generated by Django 4.1.1 on 2022-09-16 17:29

from django.db import migrations, models
import drug.models


class Migration(migrations.Migration):

    dependencies = [
        ("drug", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prescription",
            name="image",
            field=models.ImageField(upload_to=drug.models.upload_to),
        ),
    ]
