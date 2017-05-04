from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Quantity, Product
from ..supplier.models import Warehouse, Supplier, Email
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from itertools import chain
import xlrd
import xlwt


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


class QuantityTable(ListView):
    context_object_name = 'object_list'
    template_name = 'quantity_list.html'

    queryset = []
    supplier_list = Supplier.objects.all()
    for supplier in supplier_list:
        warehouse_list = Warehouse.objects.filter(supplier=supplier)
        warehouse_list_id = list(map(lambda item: item.pk, warehouse_list))
        non_empty_qty = Quantity.objects.filter(warehouse__in=warehouse_list)
        non_empty_qty = list(filter(lambda item: item.quantity > 0, non_empty_qty))
        if len(non_empty_qty) > 0:
            queryset.extend(non_empty_qty)






