from django.contrib import admin
from django.db.models import Count

from . import models


@admin.register(models.Collection)
class AdminCollection(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='product_count')
    def products_count(self, collection):
        return collection.product_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )


@admin.register(models.Product)
class AdminProduct(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'unit_price',
        'inventory_status',
        'collections_title'
    ]
    list_display_links = ['description']
    list_editable = ['title', 'unit_price']
    list_per_page = 25
    list_select_related = ['collections']

    def collections_title(self, product):
        return product.collections.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'


@admin.register(models.Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'phone', 'membership']
    list_display_links = ['first_name']
    list_editable = ['membership', 'email']
    list_per_page = 10


@admin.register(models.Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer_title']
    list_select_related = ['customer']

    def customer_title(self, order):
        return f'{order.customer.first_name} {order.customer.last_name}'

    list_per_page = 10
