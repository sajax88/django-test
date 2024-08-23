from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from sales.filters import SalesListFilter
from sales.models import SalesRecord
from sales.serializers import SalesListSerializer


class SalesListView(ListAPIView):
    queryset = SalesRecord.objects.select_related("product")
    serializer_class = SalesListSerializer
    filterset_class = SalesListFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ("date_of_sale", "quantity_sold", "total_sales_amount")
    ordering = ("-date_of_sale",)


# TODO: aggregation - remove paginator = None, ListAPIView, custome queryset and serializer
