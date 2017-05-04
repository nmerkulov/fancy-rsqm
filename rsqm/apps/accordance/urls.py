from django.conf.urls import url
from .views import supplier_list, upload_quantity, StockTable, download_file

urlpatterns = [
    url(r'^upload/(?P<supplier_id>\d+)/$', upload_quantity),
    url(r'^upload/$', supplier_list),
    url(r'^stock/$', StockTable.as_view()),
    url(r'^download/$', download_file, name='download_stock'),
]
