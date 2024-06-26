# Generated by Django 5.0.6 on 2024-06-06 16:12

import django.db.models.deletion
import django.utils.timezone
import hashid_field.field
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_remove_address_zipcode"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    hashid_field.field.HashidAutoField(
                        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                        min_length=20,
                        prefix="",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("content", models.CharField(max_length=255, null=True)),
                ("ref", models.CharField(max_length=100, null=True)),
                ("seen", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]