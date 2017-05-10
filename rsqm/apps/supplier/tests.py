from django.test import TestCase, Client
from apps.supplier.models import Supplier


class ValidateSupplierCard(TestCase):

    def test_validate_columns_equal(self):
        c = Client()
        response = c.post('/supplier/add/',
                         {'name': 'testname',
                          'column_remain': 1,
                          'column_code': 1})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Supplier.objects.filter(name='testname',
                                                 column_remain=1,
                                                 column_code=1).exists())

