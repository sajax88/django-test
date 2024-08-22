from django.urls import path

from sales import views

app_name = "programs"

urlpatterns = [
    path("", views.SalesListView.as_view(), name="sales-list"),
    # TODO path("/aggregate/", views.SalesAggregationView.as_view(), name="sales-aggregation"),
]
