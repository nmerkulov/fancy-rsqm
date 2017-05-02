from ...supplier.models import Warehouse, Supplier, Email
from ..models import Product


def initdb(size=3):

    suppliers_id_list = []

    def testinitdb(num):
        num = str(num)
        product = Product(code=1001 * (int(num) + 1))
        product.save()
        tmpsupplier = Supplier(name='supplier ' + num)
        tmpsupplier.save()
        suppliers_id_list.append(tmpsupplier.pk)
        tmpemail = Email(supplier=tmpsupplier, email='s@s' + num + '.ru')
        tmpemail.save()
        tmpwarehouse = Warehouse(supplier=tmpsupplier, name='warehouse ' + num, city='city ' + num)
        tmpwarehouse.save()

    for i in range(size):
        testinitdb(i)

    return suppliers_id_list
