from ...supplier.models import Warehouse, Supplier, Email
from ..models import Quantity
from ..models import Product


def initdb(size=3):

    suppliers_list = []

    def testinitdb(num):
        num = str(num)
        product = Product(code=1001 * (int(num) + 1))
        product.save()
        tmpsupplier = Supplier(name='supplier ' + num, column_remain=int(num), column_code=int(num))
        tmpsupplier.save()
        suppliers_list.append(tmpsupplier)
        tmpemail = Email(supplier=tmpsupplier, email='s@s' + num + '.ru')
        tmpemail.save()
        tmpwarehouse = Warehouse(supplier=tmpsupplier, name='warehouse ' + num, city='city ' + num)
        tmpwarehouse.save()
        tmpqty = Quantity(product=product, warehouse=tmpwarehouse, quantity=int(num)*1000)
        tmpqty.save()

    for i in range(size):
        testinitdb(i)

    return suppliers_list


