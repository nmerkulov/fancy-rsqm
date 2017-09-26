from django.conf.urls import url
from .views import (edit_supplier_card,
                                 SupplierListView,
                                 SupplierDetailView,
                                 add_supplier_card,
                                 delete_supplier_card,
                                 upload_matches,
                                 search_cards
                                 )


urlpatterns = [
    url(r'^$', SupplierListView.as_view(), name='sup_list'),
    url(r'^(?P<pk>\d+)/$', SupplierDetailView.as_view()),
    url(r'^add/$', add_supplier_card, name='add_card'),
    url(r'^(?P<s_id>\d+)/edit/$', edit_supplier_card, name='edit_card'),
    url(r'^(?P<s_id>\d+)/delete/$', delete_supplier_card, name='delete_card'),
    url(r'^(?P<s_id>\d+)/upload_match/$', upload_matches, name='upload_match'),
    url(r'^search/$', search_cards, name='search'), 
]