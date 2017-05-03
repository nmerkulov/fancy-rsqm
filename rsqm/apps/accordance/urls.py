from django.conf.urls import url
from .views import supplier_list, upload_quantity, QuantityTable

urlpatterns = [
    url(r'^upload/(?P<supplier_id>\d+)/$', upload_quantity),
    url(r'^upload/$', supplier_list),
    url(r'^stock/$', QuantityTable.as_view()),
]
