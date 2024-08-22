from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class TestSalesAggregation(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        # TODO: Fixtures

    def test_sales_aggregated_by_month_response_format(self):
        self.fail()  # TODO: Group the results by month

    def test_sales_aggregated_by_category_response_format(self):
        self.fail()  # TODO: Group the results by category

    def test_sales_list_category_filter(self):
        self.fail()  # TODO: category, empty filer

    def test_sales_list_date_range_filter(self):
        self.fail()  # TODO: filter by category
