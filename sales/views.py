from django.shortcuts import render
from rest_framework.generics import ListAPIView

from sales.models import SalesRecord


class SalesListView(ListAPIView):
    queryset = SalesRecord.objects.all()
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
