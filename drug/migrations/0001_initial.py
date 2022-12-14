# Generated by Django 4.1.1 on 2022-09-16 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Drug",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=555)),
            ],
        ),
        migrations.CreateModel(
            name="DrugSubsets",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("melh", models.CharField(default="", max_length=255)),
                ("drug_form", models.CharField(default="", max_length=255)),
                ("dose", models.CharField(default="", max_length=255)),
                ("route_of_admin", models.CharField(default="", max_length=255)),
                ("atc_code", models.CharField(default="", max_length=255)),
                ("ingredient", models.CharField(default="", max_length=255)),
                ("clinical", models.CharField(default="", max_length=255)),
                ("access_level", models.CharField(default="", max_length=255)),
                ("remarks", models.CharField(default="", max_length=255)),
                ("date", models.CharField(default="", max_length=255)),
                (
                    "drug",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="drug.drug",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Prescription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="prescriptions")),
            ],
        ),
        migrations.CreateModel(
            name="PrescriptionItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("count", models.IntegerField(null=True)),
                ("per_time", models.CharField(max_length=255, null=True)),
                (
                    "drug",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="drug.drugsubsets",
                    ),
                ),
            ],
        ),
    ]
