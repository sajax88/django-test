from django_filters import rest_framework as rest_framework_filters


class CategoryFilter(rest_framework_filters.CharFilter):
    empty_value = "NONE"

    def filter(self, qs, value):
        if value != self.empty_value:
            return super().filter(qs, value)

        qs = self.get_method(qs)(**{"%s__%s" % (self.field_name, self.lookup_expr): ""})
        return qs.distinct() if self.distinct else qs


class SalesListFilter(rest_framework_filters.FilterSet):
    # Use custom filter with empty value:
    # we also want to be able to look for the products without category
    category = CategoryFilter(field_name="product__category")
    start_date = rest_framework_filters.DateFilter(
        field_name="date_of_sale__date", lookup_expr="gte"
    )
    end_date = rest_framework_filters.DateFilter(
        field_name="date_of_sale__date", lookup_expr="lte"
    )


class SalesAggregationFilter(rest_framework_filters.FilterSet):
    # Use custom filter with empty value:
    # we also want to be able to look for the products without category
    category = CategoryFilter(field_name="product__category")
    start_date = rest_framework_filters.DateFilter(
        field_name="date_of_sale__date", lookup_expr="gte"
    )
    end_date = rest_framework_filters.DateFilter(
        field_name="date_of_sale__date", lookup_expr="lte"
    )
