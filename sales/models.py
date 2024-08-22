import uuid

from django.db import models


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=128, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class SalesRecord(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity_sold = models.PositiveSmallIntegerField(default=0)
    total_sales_amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_of_sale = models.DateTimeField()

    def __str__(self):
        return f"Sale on {self.date_of_sale}"
