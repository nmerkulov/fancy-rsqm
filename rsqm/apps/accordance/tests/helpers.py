from ...supplier.models import Warehouse, Supplier, Email
from ..models import Product


def initdb(size=3):

    def testinitdb(num):
        num = str(num)
        product = Product(code=1001 * (int(num) + 1))
        product.save()
        tmpsupplier = Supplier(name='supplier ' + num)
        tmpsupplier.save()
        tmpemail = Email(supplier=tmpsupplier, email='s@s' + num + '.ru')
        tmpemail.save()
        tmpwarehouse = Warehouse(supplier=tmpsupplier, name='warehouse ' + num, city='city ' + num)
        tmpwarehouse.save()

    for i in range(size):
        testinitdb(i)
