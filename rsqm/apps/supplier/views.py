from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from apps.supplier.models import Supplier
from apps.accordance.models import Product, Match
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from apps.supplier.forms import SupplierForm, EmailFormSet, MatchesUploadForm
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
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
            count_success = 0
            count_failed = 0
            for rownum in range(sheet.nrows):
                row = sheet.row_values(rownum)
                try:
                    product = Product.objects.get(code=int(row[0]))
                    match = Match.objects.get_or_create(
                                              supplier_code=int(row[1]),
                                              supplier_id=s_id,
                                              product_id=product.id)
                    count_success += 1
                except ObjectDoesNotExist:
                    count_failed += 1
            msg = 'Successful recognized {}, Not recognized {}'.format(count_success, count_failed)
            return render(request, 'upload.html', {'upload_form': upload_form,
                                                   'msg':msg})
    else:
        upload_form = MatchesUploadForm()
    return render(request, 'upload.html', {'upload_form': upload_form})


def add_supplier_card(request):
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)
        # supplier_instance = supplier_form.save(commit=False)
        email_formset = EmailFormSet(prefix='emails')
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
        'email_formset': email_formset})


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


def search_cards(request):
    query = request.GET.get('q')
    if query and query != '' and request.is_ajax():
        suppliers_search = Supplier.objects.filter(
            Q(name__startswith=query)
        )
        return render(request, 'ajax_search.html',
                               {'suppliers_search': suppliers_search})
    elif query == '' and request.is_ajax():
        suppliers_search = Supplier.objects.all()
        return render(request, 'ajax_search.html',
                               {'suppliers_search': suppliers_search})

    return(render, 'ajax_search.html')
