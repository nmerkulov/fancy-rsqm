from django.conf.urls import url
from .views import supplier_list, upload_quantity, StockTable

urlpatterns = [
    url(r'^upload/(?P<supplier_id>\d+)/$', upload_quantity),
    url(r'^(?P<s_id>\d+)/upload_quant/$', upload_quantity, name='upload_quant'),
    url(r'^upload/$', supplier_list),
    url(r'^stock/$', StockTable.as_view(), name='quan_list'),
]
