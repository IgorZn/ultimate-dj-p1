from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>10', 'OK')

        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == 'OK':
            return queryset.filter(inventory__gte='10')


@admin.register(models.Collection)
class AdminCollection(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': collection.id
            })
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


@admin.register(models.Product)
class AdminProduct(admin.ModelAdmin):
    actions = ['clear_inventory']
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
    list_filter = ['last_update', 'collections', InventoryFilter]

    def collections_title(self, product):
        return product.collections.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )


@admin.register(models.Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'membership', 'customer_orders']
    list_display_links = ['first_name']
    list_editable = ['membership', 'email']
    list_per_page = 10
    search_fields = ['last_name__istartswith', 'first_name__istartswith']

    @admin.display(ordering='customer_orders')
    def customer_orders(self, orderitem):
        url = (
            reverse('admin:store_orderitem_changelist')
            + '?'
            + urlencode({
                'order__id': orderitem.id
            })
        )
        return format_html('<a href="{}">{}</a>', url, orderitem.customer_orders)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            customer_orders=Count('order')
        )


@admin.register(models.Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer_title']
    list_select_related = ['customer']

    def customer_title(self, order):
        return f'{order.customer.first_name} {order.customer.last_name}'

    list_per_page = 10


@admin.register(models.OrderItem)
class AdminOrderItem(admin.ModelAdmin):
    list_display = ['quantity', 'order_id', 'product_id']
