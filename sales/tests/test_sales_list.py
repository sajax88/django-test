from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class TestSalesList(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        # TODO: Fixtures

    def test_sales_list_response_format(self):
        self.fail()  # TODO: returned structure check

    def test_sales_list_category_filter(self):
        self.fail()  # TODO: category, empty filer

    def test_sales_list_date_range_filter(self):
        self.fail()  # TODO: filter by category
