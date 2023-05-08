# Generated by Django 4.1.2 on 2023-05-08 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0001_initial"),
        ("labs", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lab",
            name="linked_post",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="articles.post",
            ),
        ),
    ]
