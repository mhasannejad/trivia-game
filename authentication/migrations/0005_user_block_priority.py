# Generated by Django 4.1.1 on 2023-02-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0004_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="block_priority",
            field=models.IntegerField(default=1),
        ),
    ]