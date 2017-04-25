from django.conf.urls import url
from .views import test, initdb, generatexls, supplier_list, upload_quantity

urlpatterns = [
    url(r'^(\d+)/$', upload_quantity),
    url(r'^', supplier_list),
]
