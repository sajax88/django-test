from rest_framework import serializers

from sales.models import Product, SalesRecord


class ProductNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
        ]


class SalesListSerializer(serializers.ModelSerializer):
    product = ProductNestedSerializer()

    class Meta:
        model = SalesRecord
        fields = [
            "id",
            "product",
            "quantity_sold",
            "total_sales_amount",
            "date_of_sale",
        ]
