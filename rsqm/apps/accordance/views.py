from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Quantity, Product
from ..supplier.models import Warehouse, Supplier, Email
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from django.db.models import Max
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
        for item in row:
            try:
                wareh = Warehouse.objects.get(pk=int(warehouse_id))
                try:
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
        if error_file_flag:
            for item in qty_to_save:
                item.save()
            message.append('welldone')
        message = ' '.join(message)
        return HttpResponse(message)


class StockTable(ListView):
    context_object_name = 'object_list'
    template_name = 'quantity_list.html'

    def get_queryset(self):
        return my_get_queryset()


def my_get_queryset():
    queryset = Warehouse.objects.filter(quantity__quantity__gt=0).annotate(max_quantity=Max('quantity__quantity')).select_related('supplier')
    return queryset







