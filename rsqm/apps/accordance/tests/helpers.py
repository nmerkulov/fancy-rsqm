from ...supplier.models import Warehouse, Supplier, Email
from ..models import Quantity
from ..models import Product


def initdb_accordance_test_case(size=3):

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


def initdb_stocktable_test_case(size=3):
    def create_nonempty_supplier():
        product = Product(code=1000)
        product.save()
        tmpsupplier = Supplier(name='nonempty supplier', column_remain=0, column_code=0)
        tmpsupplier.save()
        suppliers_list['nonempty'] = tmpsupplier
        tmpemail = Email(supplier=tmpsupplier, email='s@s.ru')
        tmpemail.save()
        tmpwarehouse = Warehouse(supplier=tmpsupplier, name='warehouse 1', city='city 1')
        tmpwarehouse.save()
        tmpqty = Quantity(product=product, warehouse=tmpwarehouse, quantity=1000)
        tmpqty.save()

    def create_empty_supplier():
        product = Product(code=1001)
        product.save()
        tmpsupplier = Supplier(name='empty supplier', column_remain=1, column_code=1)
        tmpsupplier.save()
        suppliers_list['empty'] = tmpsupplier
        tmpemail = Email(supplier=tmpsupplier, email='s@k.ru')
        tmpemail.save()
        tmpwarehouse = Warehouse(supplier=tmpsupplier, name='warehouse 2', city='city 2')
        tmpwarehouse.save()
        tmpqty = Quantity(product=product, warehouse=tmpwarehouse, quantity=0)
        tmpqty.save()

    suppliers_list = {}
    create_nonempty_supplier()
    create_empty_supplier()
    return suppliers_list


