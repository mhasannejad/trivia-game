# Generated by Django 4.1.1 on 2023-02-25 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leitner", "0003_daroo_block"),
    ]

    operations = [
        migrations.AddField(
            model_name="daroo",
            name="block_combined",
            field=models.CharField(default="", max_length=25, null=True),
        ),
    ]
