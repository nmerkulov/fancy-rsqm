from django.conf.urls import url
from .views import supplier_list, upload_quantity

urlpatterns = [
    url(r'^(?P<supplier_id>\d+)/$', upload_quantity),
    url(r'^', supplier_list),
]
