# Generated by Django 4.1.1 on 2022-09-13 13:19

from django.db import migrations, models
import unixtimestampfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_rename_right_option_question_right_answer_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="challenge",
            name="private",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="challenge",
            name="created_at",
            field=unixtimestampfield.fields.UnixTimeStampField(auto_now_add=True),
        ),
    ]
