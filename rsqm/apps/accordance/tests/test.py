from django.test import Client
from django.test import TestCase
from .helpers import initdb_accordance_test_case, initdb_stocktable_test_case
from ...supplier.models import Warehouse, Supplier, Email
from django.http import Http404


class AccordanceTestCase(TestCase):
    def setUp(self):
        self.suppliers_list = list(map(lambda item: item.pk, initdb_accordance_test_case()))

    def test_supplier_id_access_fail(self):
        c = Client()
        self.assertEqual(c.get('/quantity/upload/%d/' % (max(self.suppliers_list) + 999)).status_code, 404)

    def test_supplier_id_access_fine(self):
        c = Client()
        self.assertEqual(c.get('/quantity/upload/%d/' % self.suppliers_list[0]).status_code, 200)


class StockTableTestCase(TestCase):
    def setUp(self):
        self.suppliers_list = initdb_stocktable_test_case()

    def test_supplier_empty(self):
        c = Client()
        response = c.get('/quantity/stock/')
        supplier_flag = False
        for item in response.context['object_list']:
            if item.supplier == self.suppliers_list['empty']:
                supplier_flag = True
                break
        self.assertFalse(supplier_flag)

    def test_supplier_non_empty(self):
        c = Client()
        response = c.get('/quantity/stock/')
        supplier_flag = False
        for item in response.context['object_list']:
            if item.supplier == self.suppliers_list['nonempty']:
                supplier_flag = True
                break
        self.assertTrue(supplier_flag)
