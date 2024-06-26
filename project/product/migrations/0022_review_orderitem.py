# Generated by Django 5.0.6 on 2024-06-12 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0021_review"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="orderItem",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="product.orderitem",
            ),
        ),
    ]