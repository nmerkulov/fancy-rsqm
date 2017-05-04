from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Quantity, Product
from ..supplier.models import Warehouse, Supplier, Email
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
import xlrd
import xlwt


def download_file(request):
    queryset = my_get_queryset()

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Stock Table')

    data_for_xls = list(queryset['stock'])
    for index, item in enumerate(data_for_xls):
        ws.write(index, 0, item.warehouse.name)
        ws.write(index, 1, item.product.code)
        ws.write(index, 2, item.quantity)
        ws.write(index, 3, '%d.%d.%d' % (item.date.day, item.date.month, item.date.year))

    response = HttpResponse(content_type='application/excel')
    response['Content-Disposition'] = 'attachment; filename=example.xls'
    response['Content-Type'] = 'application/excel'
    wb.save(response)
    return response


def supplier_list(request):
    context = {
        'object_list': Supplier.objects.all()
    }
    return render(request, 'supplier_list.html', context)


def upload_quantity(request, supplier_id):
    if request.method == 'GET':
        supplier = get_object_or_404(Supplier, pk=supplier_id)
        context = {
            'object_list': Warehouse.objects.filter(supplier=supplier)
        }
        return render(request, 'upload_quantity.html', context)

    elif request.method == 'POST':
        input_excel = request.FILES['quantity']
        book = xlrd.open_workbook(file_contents=input_excel.read())
        sheet = book.sheet_by_index(0)
        warehouse_id = request.POST['warehouse']
        row = []
        message = []
        error_file_flag = True
        qty_to_save = []
        for rownum in range(sheet.nrows):
            row.append(sheet.row_values(rownum))
        print(len(row))
        for item in row:
            print('in row', len(row))
            try:
                print('wareh')
                wareh = Warehouse.objects.get(pk=int(warehouse_id))
                try:
                    print(item[0])
                    prod = Product.objects.get(code=int(item[0]))
                    try:
                        qty = Quantity.objects.get(warehouse=wareh, product=prod)
                        qty.quantity = int(item[1])
                        qty_to_save.append(qty)
                    except ObjectDoesNotExist:
                        qty = Quantity(warehouse=wareh, product=prod, quantity=int(item[1]))
                        qty_to_save.append(qty)
                except ObjectDoesNotExist:
                    error_file_flag = False
                    message.append('no such product in base ' + str(int(item[0])) + ' ')
            except ObjectDoesNotExist:
                error_file_flag = False
                message.append('unknown warehouse, check your input doc')
        print(error_file_flag)
        if error_file_flag:
            for item in qty_to_save:
                item.save()
            message.append('welldone')
        message = ' '.join(message)
        print(message)
        return HttpResponse(message)


class StockTable(ListView):
    context_object_name = 'object_list'
    template_name = 'quantity_list.html'

    def get_queryset(self):
        return my_get_queryset()


def my_get_queryset():
    queryset = {
        'suppliers': [],
        "stock": []
    }
    supplier_list = Supplier.objects.all()
    for supplier in supplier_list:
        warehouse_list = Warehouse.objects.filter(supplier=supplier)
        non_empty_qty = Quantity.objects.filter(warehouse__in=warehouse_list)
        if len(list(filter(lambda item: item.quantity > 0, non_empty_qty))) > 0:
            queryset['stock'].extend(non_empty_qty)
            queryset['suppliers'].append(supplier)
    return queryset







