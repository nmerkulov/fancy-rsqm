from django.test import TestCase, Client


class ValidateSupplierCard(TestCase):
    # def setUp(self):
        # pass

    def test_validate_columns_equal(self):
        c = Client()
        response = c.post('/supplier/add/',
                         {'name': 'testname',
                          'column_remain': 1,
                          'column_code': 1})
        self.assertEqual(response.status_code, 200)


    # def test_validate_columns_not_equal(self):
    #     c = Client()
    #     response = c.post('/supplier/add/',
    #                      {'name': 'bbb',
    #                       'column_remain': 1,
    #                       'column_code': 2})
    #     self.assertEqual(response.status_code, 302)
