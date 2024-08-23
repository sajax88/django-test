from django.db.models import (
    CharField,
    DecimalField,
    ExpressionWrapper,
    F,
    Func,
    QuerySet,
    Sum,
    TextChoices,
    Value,
)
from django.db.models.sql import Query
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from sales.filters import SalesAggregationFilter, SalesListFilter
from sales.models import SalesRecord
from sales.serializers import SalesAggregatedSerializer, SalesListSerializer


class SalesListView(ListAPIView):
    queryset = SalesRecord.objects.select_related("product")
    serializer_class = SalesListSerializer
    filterset_class = SalesListFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ("date_of_sale", "quantity_sold", "total_sales_amount")
    ordering = ("-date_of_sale",)


class AggregationChoices(TextChoices):
    MONTH = "month", "Month"
    CATEGORY = "category", "Category"


class SalesAggregationView(ListAPIView):
    queryset = SalesRecord.objects.select_related("product")
    pagination_class = None
    serializer_class = SalesAggregatedSerializer
    filterset_class = SalesAggregationFilter

    def list(self, request, *args, **kwargs):
        aggregation_type = kwargs.get("aggregation_type")
        if aggregation_type not in AggregationChoices.values:
            raise Http404("Invalid aggregation type")

        queryset = self.filter_queryset(self.get_queryset())
        aggregated_data = self.aggregate_data(queryset, aggregation_type)
        serializer = self.get_serializer(aggregated_data, many=True)
        return Response(serializer.data)

    @staticmethod
    def aggregate_data(queryset, aggregation_type: str) -> QuerySet:
        if aggregation_type == AggregationChoices.MONTH:
            group_field_name = "year_and_month"
            queryset = queryset.annotate(
                year_and_month=Func(
                    F("date_of_sale"),
                    Value("YYYY-MM"),
                    function="to_char",
                    output_field=CharField(),
                )
            )
        elif aggregation_type == AggregationChoices.CATEGORY:
            group_field_name = "product__category"
        else:
            raise ValueError("Invalid aggregation type")

        queryset = (
            queryset.values(group_field_name)
            .annotate(
                total_sales=Sum("total_sales_amount"),
                total_quantity=Sum("quantity_sold"),
                average_price=ExpressionWrapper(
                    F("total_sales") / F("total_quantity"),
                    output_field=DecimalField(max_digits=8, decimal_places=2),
                ),
            )
            .annotate(group=F(group_field_name))
            .order_by("group")
        )

        return queryset
