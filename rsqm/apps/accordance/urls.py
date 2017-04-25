from django.conf.urls import url
from .views import test, initdb, generatexls, supplierform, warehouseform

urlpatterns = [
    url(r'^new/', test),
    url(r'^initdb/', initdb),
    url(r'^genxl/', generatexls),

    url(r'^rest/(.*?)/', warehouseform),
    url(r'^rest/', supplierform),
]
