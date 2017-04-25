from django.shortcuts import render
from django.http import HttpResponse
from .models import Quantity, Product
from ..supplier.models import Warehouse, Supplier, Email
from django.core.exceptions import ObjectDoesNotExist
import xlrd
import xlwt

def test(request):
    path = 'C:/Users/mnk2/my-project/fancy-rsqm/example.xls'
    try:
        a = xlrd.open_workbook(path)
    except IOError:
        generatexls(request, path)
        a = xlrd.open_workbook(path)
    sheet = a.sheet_by_index(0)
    row = []
    message = []
    try:
        supplier = Supplier.objects.get(name='supplier 1')
    except ObjectDoesNotExist:
        initdb(request, size=3)

    for rownum in range(sheet.nrows):
        row.append(sheet.row_values(rownum))
    if row[0] == ['Product', 'Quantity', 'Warehouse']:
        print(row, 'row')
        row = row[1:]
        print(row, 'row')
        for item in row:
            print('in row', len(row))
            try:
                print('warehouse')
                wareh = Warehouse.objects.get(name=str(item[2]))
                try:
                    print('product')
                    prod = Product.objects.get(code=int(item[0]))
                    try:
                        qty = Quantity(warehouse=wareh, product=prod)
                        qty.quantity = int(item[1])
                        qty.save()
                        message.append(qty.quantity)
                    except ObjectDoesNotExist:
                        Quantity.objects.create(werehouse=wareh, prduct=prod, quantity=int(item[1]))
                        message.append('new entry', item)
                except ObjectDoesNotExist:
                    print(int(item[0]))
                    message.append('no such product in base ' + str(int(item[0])) + ' ')
            except ObjectDoesNotExist:
                message.append('unknown warehouse, check your input doc' + str(item[2] + ' '))

    return HttpResponse(''.join(message))


def initdb(request, size=3):

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

    return HttpResponse('db init success')


def generatexls(request, path = 'example.xls'):

    def fillxlrow(rownum, table):
        rownum = int(rownum)
        table.write(rownum + 1, 0, 1001 * (i + 1))
        table.write(rownum + 1, 1, 11 * (i + 1))
        table.write(rownum + 1, 2, 'warehouse ' + str(rownum))

    xl = xlwt.Workbook()
    xls = xl.add_sheet('supplier rest')
    col = ['Product', 'Quantity', 'Warehouse']
    for index, colname in enumerate(col):
        xls.write(0, index, colname)

    for i in range(3):
        fillxlrow(i, xls)

    print(xl.save(path))

    return HttpResponse('generated xls')


def supplierform(request):
    print('supplier form')
    supplier = Supplier.objects.all()
    context = {
        'supplier': []
    }
    for item in supplier:
        context['supplier'].append(item)
    return render(request, 'supplier_form.html', context)


def warehouseform(request, *args):
    print(args)
    supplier = args[0]
    supplier = Supplier.objects.get(name=supplier)
    print(supplier)
    warehouse = Warehouse.objects.filter(supplier=supplier)

    context = {
        'warehouse': []
    }
    for item in warehouse:
        context['warehouse'].append(item.name)
    return render(request, 'warehouse_form.html', context)




