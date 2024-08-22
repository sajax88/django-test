# Generated by Django 5.1 on 2024-08-22 07:34

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("category", models.CharField(blank=True, max_length=128)),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name="SalesRecord",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("quantity_sold", models.PositiveSmallIntegerField(default=0)),
                (
                    "total_sales_amount",
                    models.DecimalField(decimal_places=2, max_digits=8),
                ),
                ("date_of_sale", models.DateTimeField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="sales.product"
                    ),
                ),
            ],
        ),
    ]
