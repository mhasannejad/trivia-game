# Generated by Django 4.1.1 on 2023-02-25 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leitner", "0002_daroo_flashcard"),
    ]

    operations = [
        migrations.AddField(
            model_name="daroo",
            name="block",
            field=models.IntegerField(default=0, null=True),
        ),
    ]
