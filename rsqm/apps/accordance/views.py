from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Quantity, Product
from ..supplier.models import Warehouse, Supplier, Email
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from django.db.models import Sum
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
    queryset = Warehouse.objects.filter(quantity__quantity__gt=0).annotate(sum_quantity=Sum('quantity__quantity')).select_related('supplier')







