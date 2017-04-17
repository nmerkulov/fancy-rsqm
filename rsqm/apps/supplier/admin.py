from django.contrib import admin
from .models import Warehouse, Email, Supplier


class EmailInline(admin.StackedInline):
    model = Email


class WarehouseInline(admin.StackedInline):
    model = Warehouse


class SupplierAdmin(admin.ModelAdmin):
    inlines = [
        EmailInline,
        WarehouseInline,
    ]


admin.site.register(Warehouse)
admin.site.register(Email)
admin.site.register(Supplier, SupplierAdmin)
# Register your models here.
