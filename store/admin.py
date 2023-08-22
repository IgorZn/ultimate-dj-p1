from django.contrib import admin

from . import models


@admin.register(models.Collection)
class AdminCollection(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class AdminProduct(admin.ModelAdmin):
    pass
