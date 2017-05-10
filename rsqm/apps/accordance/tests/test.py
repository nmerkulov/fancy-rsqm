from django.test import Client
from django.test import TestCase
from .helpers import initdb
from django.http import Http404


class AccordanceTestCase(TestCase):
    def setUp(self):
        self.suppliers_id_list = initdb(3)

    def test_supplier_id_access_fail(self):
        c = Client()
        self.assertEqual(c.get('/supply/%d/' % (max(self.suppliers_id_list) + 1)).status_code, 404)

    def test_supplier_id_access_fine(self):
        c = Client()
        self.assertEqual(c.get('/supply/%d/' % self.suppliers_id_list[0]).status_code, 200)
