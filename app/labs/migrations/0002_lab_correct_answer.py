# Generated by Django 4.2.1 on 2023-05-15 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("labs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lab",
            name="correct_answer",
            field=models.CharField(default="", max_length=1024),
            preserve_default=False,
        ),
    ]