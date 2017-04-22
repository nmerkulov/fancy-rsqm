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
        row = row[1:0]
        for item in row:
            try:
                wareh = Warehouse.objects.get(name=str(item[2]))
                try:
                    prod = Product(code=int(item[0]))
                    try:
                        qty = Quantity(warehouse=wareh, product=prod)
                        qty.quantity = int(item[1])
                        qty.save()
                    except ObjectDoesNotExist:
                        Quantity.objects.create(werehouse=wareh, prduct=prod, quantity=int(item[1]))
                        message.append('new entry', item)
                except ObjectDoesNotExist:
                    message.append('no such product in base', item[0])
            except ObjectDoesNotExist:
                message.append('unknown warehouse, check your input doc', item[2])

    return HttpResponse(message)


def initdb(request, size=3):

    def testinitdb(num):
        num = str(num)
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




