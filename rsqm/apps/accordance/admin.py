from django.contrib import admin
from .models import Product, Match, Quantity


admin.site.register(Product)
admin.site.register(Match)
admin.site.register(Quantity)