# Generated by Django 5.0.6 on 2024-06-15 07:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0027_remove_review_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="productcategory",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]