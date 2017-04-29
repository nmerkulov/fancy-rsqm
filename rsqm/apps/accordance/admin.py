from django.contrib import admin
from .models import Product, Match, Quantity


class QuantityAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity']


class MatchAdmin(admin.ModelAdmin):
    list_display = ['product', 'supplier_code', 'supplier']



admin.site.register(Product)
admin.site.register(Match, MatchAdmin)
admin.site.register(Quantity, QuantityAdmin)
