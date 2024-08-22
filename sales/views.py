from django.shortcuts import render
from rest_framework.generics import ListAPIView

from sales.filters import SalesListFilter
from sales.models import SalesRecord
from sales.serializers import SalesListSerializer


class SalesListView(ListAPIView):
    queryset = SalesRecord.objects.select_related("product").all()
    serializer_class = SalesListSerializer
    filterset_class = SalesListFilter
    ordering_fields = ("date_of_sale", "quantity_sold", "total_sales_amount")
    ordering = ("-date_of_sale",)
