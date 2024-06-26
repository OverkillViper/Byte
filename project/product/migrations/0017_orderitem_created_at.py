# Generated by Django 5.0.6 on 2024-06-04 15:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0016_orderitem_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]