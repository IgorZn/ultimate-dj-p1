from django.contrib import admin

from . import models


@admin.register(models.Collection)
class AdminCollection(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'description', 'unit_price', 'inventory_status']
    list_display_links = ['description']
    list_editable = ['title', 'unit_price']
    list_per_page = 25

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