import datetime
from decimal import Decimal

import pytz
from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import F, G
from rest_framework.test import APIClient

from sales.models import SalesRecord


class TestSalesAggregation(TestCase):

    def setUp(self) -> None:
        # For response comparison
        self.maxDiff = None

        self.client = APIClient()

        # Total sales for Jan 2024: 1400, avg price = 1400/6 = 233.33
        G(
            SalesRecord,
            quantity_sold=4,
            total_sales_amount=400,
            date_of_sale=datetime.datetime(2024, 1, 5, tzinfo=pytz.utc),
            product=F(category=""),
        )
        G(
            SalesRecord,
            quantity_sold=2,
            total_sales_amount=1000,
            date_of_sale=datetime.datetime(2024, 1, 20, tzinfo=pytz.utc),
            product=F(category="rubber ducks"),
        )

        # Total sales for Feb 2024: 3000, avg price = 3000/20 = 150
        G(
            SalesRecord,
            quantity_sold=8,
            total_sales_amount=1000,
            date_of_sale=datetime.datetime(2024, 2, 3, tzinfo=pytz.utc),
            product=F(category=""),
        )

        G(
            SalesRecord,
            quantity_sold=12,
            total_sales_amount=2000,
            date_of_sale=datetime.datetime(2024, 2, 20, tzinfo=pytz.utc),
            product=F(category="rubber ducks"),
        )

    def test_sales_aggregated_by_month(self):
        expected_response = [
            {
                "group": "2024-01",
                "total_sales": Decimal("1400.00"),
                "average_price": Decimal("233.33"),
            },
            {
                "group": "2024-02",
                "total_sales": Decimal("3000.00"),
                "average_price": Decimal("150.00"),
            },
        ]
        response = self.get_sales_aggregation("month")
        self.assertEqual(expected_response, response.data)

    def test_sales_aggregated_by_category(self):
        expected_response = [
            {
                "group": "",
                "total_sales": Decimal("1400.00"),
                "average_price": Decimal("116.67"),
            },
            {
                "group": "rubber ducks",
                "total_sales": Decimal("3000.00"),
                "average_price": Decimal("214.29"),
            },
        ]
        response = self.get_sales_aggregation("category")
        self.assertEqual(expected_response, response.data)

    def test_sales_list_category_filter(self):
        expected_response = [
            {
                "group": "2024-01",
                "total_sales": Decimal("1000.00"),
                "average_price": Decimal("500.00"),
            },
            {
                "group": "2024-02",
                "total_sales": Decimal("2000.00"),
                "average_price": Decimal("166.67"),
            },
        ]
        response = self.get_sales_aggregation("month", {"category": "rubber ducks"})
        self.assertEqual(expected_response, response.data)

    def test_sales_list_date_range_filter(self):
        expected_response = [
            {
                "group": "2024-01",
                "total_sales": Decimal("1000.00"),
                "average_price": Decimal("500.00"),
            },
            {
                "group": "2024-02",
                "total_sales": Decimal("1000.00"),
                "average_price": Decimal("125.00"),
            },
        ]
        response = self.get_sales_aggregation(
            "month", {"start_date": "2024-01-20", "end_date": "2024-02-3"}
        )
        self.assertEqual(expected_response, response.data)

    def test_sales_list_invalid_aggregation_type(self):
        response = self.get_sales_aggregation("INVALID")
        self.assertEqual(404, response.status_code)
        self.assertEqual("Invalid aggregation type", response.data["detail"])

    def get_sales_aggregation(self, type: str, data=None):
        return self.client.get(
            reverse("sales:sales-aggregation", kwargs={"aggregation_type": type}),
            data=data,
        )
