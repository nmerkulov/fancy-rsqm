from django.contrib import admin
from .models import A

admin.site.register(A, admin.ModelAdmin)
