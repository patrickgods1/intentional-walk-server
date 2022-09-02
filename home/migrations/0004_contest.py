# Generated by Django 3.0.5 on 2020-04-26 19:04

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_auto_20200426_0613"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contest",
            fields=[
                (
                    "contest_id",
                    models.CharField(
                        default=uuid.uuid4,
                        max_length=250,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("start", models.DateField()),
                ("end", models.DateField()),
            ],
            options={
                "ordering": ("-start",),
            },
        ),
    ]
