# Generated by Django 5.0.6 on 2024-05-24 06:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_alter_category_parent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="product.category",
            ),
        ),
    ]
