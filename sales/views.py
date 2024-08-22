from django.shortcuts import render
from rest_framework.generics import ListAPIView

from sales.models import SalesRecord
from sales.serializers import SalesListSerializer


class SalesListView(ListAPIView):
    queryset = SalesRecord.objects.select_related("product").all()
    serializer_class = SalesListSerializer

    # TODO: select with product
    """
    Input Parameters:
    start_date: Filter sales starting from this date.
    end_date: Filter sales up to this date.
    category: Filter sales by product category.
    """

    # TODO
    # filterset_class
    # order by
    # pagination
