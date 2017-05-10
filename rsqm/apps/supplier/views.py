from django.shortcuts import render, redirect, get_object_or_404
from apps.supplier.models import Supplier
from apps.accordance.models import Product, Match
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from apps.supplier.forms import SupplierForm, EmailFormSet, MatchesUploadForm
from django.http import HttpResponse, HttpResponseRedirect
import xlrd


class SupplierListView(ListView):
    context_object_name = 'supplier_list'
    model = Supplier


class SupplierDetailView(DetailView):
    model = Supplier


def upload_matches(request, s_id):
    if request.method == 'POST':
        upload_form = MatchesUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload_xls = request.FILES['matches']
            workbook = xlrd.open_workbook(file_contents=upload_xls.read())
            sheet = workbook.sheet_by_index(0)
            count = 0
            for rownum in range(sheet.nrows):
                row = sheet.row_values(rownum)
                product = Product.objects.create(code=int(row[0]))
                product.save()
                
                product = get_object_or_404(Product, code=int(row[0]))
                try:
                    match = Match.objects.get(supplier_code=int(row[1]),
                                              supplier_id=s_id)

                except ObjectDoesNotExist:
                    match = Match.objects.create(supplier_code=int(row[1]),
                                                 supplier_id=s_id,
                                                 product_id=product.id)
                    match.save()
                    count += 1
            return HttpResponse('Successful added {}'.format(count))
    else:
        upload_form = MatchesUploadForm()
    return render(request, 'upload.html', {'upload_form': upload_form})


def add_supplier_card(request):
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)
        if supplier_form.is_valid():
            supplier_instance = supplier_form.save()
            email_formset = EmailFormSet(request.POST or None,
                                         prefix='emails',
                                         instance=supplier_instance)
            if email_formset.is_valid():
                email_formset.save()
                return HttpResponseRedirect('/supplier/')
    else:
        supplier_form = SupplierForm()
        email_formset = EmailFormSet(prefix='emails')
    return render(request, 'management_supplier.html', {
        'supplier_form': supplier_form,
        'email_formset': email_formset, })


def edit_supplier_card(request, s_id):
    supplier_instance = get_object_or_404(Supplier, id=s_id)
    supplier_form = SupplierForm(request.POST or None,
                                 instance=supplier_instance)
    email_formset = EmailFormSet(request.POST or None,
                                 instance=supplier_instance)
    if supplier_form.is_valid() and email_formset.is_valid():
        supplier_instance = supplier_form.save()
        supplier_instance.save()
        email_formset.save()
        return HttpResponseRedirect('/supplier/')
    context = {
        'supplier_form': supplier_form,
        'supplier_instance': supplier_instance,
        'email_formset': email_formset, }
    return render(request, 'management_supplier.html', context)


def delete_supplier_card(request, s_id):
    instance = get_object_or_404(Supplier, id=s_id)
    instance.delete()
    return redirect('sup_list')
