from django.contrib import admin

from sales.models import Product, SalesRecord


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "id",
    )
    list_per_page = 50


@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_select_related = ("product",)
    list_display = (
        "date_of_sale",
        "product",
        "quantity_sold",
        "total_sales_amount",
        "id",
    )
    list_per_page = 50
