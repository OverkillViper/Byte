# Generated by Django 5.0.6 on 2024-06-09 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0018_alter_order_status_alter_orderitem_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="price",
            field=models.IntegerField(default=0),
        ),
    ]
