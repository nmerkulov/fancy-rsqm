from django.test import Client
from django.test import TestCase
from .helpers import initdb
from django.http import Http404


class AccordanceTestCase(TestCase):
    def setUp(self):
        initdb(3)

    def test_supplier_id_access_fail(self):
        c = Client()
        self.assertEqual(c.get('/supply/' + str(10) + '/').status_code, 404)

    def test_supplier_id_access_fine(self):
        c = Client()
        self.assertEqual(c.get('/supply/' + str(1) + '/').status_code, 200)
