from django.conf.urls import url
from apps.supplier.views import (edit_supplier_card,
                                 SupplierListView,
                                 SupplierDetailView,
                                 add_supplier_card,
                                 delete_supplier_card,
                                 )


urlpatterns = [
    url(r'^$', SupplierListView.as_view(), name='sup_list'),
    url(r'^(?P<pk>\d+)/$', SupplierDetailView.as_view()),
    url(r'^add/$', add_supplier_card),
    url(r'^(?P<s_id>\d+)/edit/$', edit_supplier_card),
    url(r'^(?P<s_id>\d+)/delete/$', delete_supplier_card),
    ]