# Generated by Django 4.1.2 on 2023-04-22 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="is_pinned",
            field=models.BooleanField(default=True),
        ),
    ]
