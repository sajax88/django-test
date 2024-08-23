import datetime

import pytz
from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import F, G
from rest_framework.serializers import DateTimeField as DRFDateTimeField
from rest_framework.test import APIClient

from sales.models import Product, SalesRecord


class TestSalesList(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_sales_list_response_format(self):
        # Let's create one product and one sale just to test the format
        sales_record = G(SalesRecord, product=F(category="test"))
        product = sales_record.product

        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": str(sales_record.pk),
                    "product": {
                        "id": str(product.pk),
                        "name": product.name,
                        "category": product.category,
                    },
                    "quantity_sold": sales_record.quantity_sold,
                    "total_sales_amount": sales_record.total_sales_amount,
                    "date_of_sale": DRFDateTimeField().to_representation(
                        sales_record.date_of_sale
                    ),
                }
            ],
        }

        response = self.get_sales_list()
        self.assertTrue(200, response.status_code)
        self.assertEqual(expected_response, response.data)

    def test_sales_list_category_filter(self):
        record_with_category = G(SalesRecord, product=F(category="test"))
        record_no_category = G(SalesRecord, product=F(category=""))

        # Filter by category first
        response = self.get_sales_list({"category": "test"})
        results = response.data["results"]
        self.assertEqual(1, len(results))
        self.assertEqual(str(record_with_category.id), results[0]["id"])

        # Now we want records without category
        response = self.get_sales_list({"category": "NONE"})
        results = response.data["results"]
        self.assertEqual(1, len(results))
        self.assertEqual(str(record_no_category.id), results[0]["id"])

    def test_sales_list_date_range_filter(self):
        G(SalesRecord, date_of_sale=datetime.datetime(2024, 1, 5, tzinfo=pytz.utc))
        # Check that the search range is inclusive (both start and end)
        response = self.get_sales_list(
            {"start_date": "2024-01-05", "end_date": "2024-01-06"}
        )
        self.assertEqual(1, len(response.data["results"]))

        response = self.get_sales_list(
            {"start_date": "2024-01-04", "end_date": "2024-01-05"}
        )
        self.assertEqual(1, len(response.data["results"]))

        response = self.get_sales_list(
            {"start_date": "2024-01-06", "end_date": "2024-01-06"}
        )
        self.assertEqual(0, len(response.data["results"]))

    def get_sales_list(self, data=None):
        return self.client.get(reverse("sales:sales-list"), data=data)
