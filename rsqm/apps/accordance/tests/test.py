from django.test import Client
from django.test import TestCase
from .helpers import initdb
from ...supplier.models import Warehouse, Supplier, Email
from django.http import Http404


class AccordanceTestCase(TestCase):
    def setUp(self):
        self.suppliers_list = list(map(lambda item: item.pk, initdb(3)))

    def test_supplier_id_access_fail(self):
        c = Client()
        self.assertEqual(c.get('/quantity/upload/%d/' % (max(self.suppliers_list) + 1)).status_code, 404)

    def test_supplier_id_access_fine(self):
        c = Client()
        self.assertEqual(c.get('/quantity/upload/%d/' % self.suppliers_list[0]).status_code, 200)


class StockTableTestCase(TestCase):
    def setUp(self):
        self.suppliers_list = initdb(3)

    def test_supplier_empty(self):
        c = Client()
        print(response.context)
        self.assertTrue(self.suppliers_list[1] in response.context['object_list']['suppliers'])

    def test_supplier_non_empty(self):
        c = Client()
        print(response.context)
        self.assertFalse(self.suppliers_list[0] in response.context['object_list']['suppliers'])
