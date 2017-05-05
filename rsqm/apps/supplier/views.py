from django.shortcuts import render, redirect, get_object_or_404
from apps.supplier.models import Supplier
from django.views.generic import ListView, DetailView
from apps.supplier.forms import SupplierForm, EmailFormSet
from django.http import HttpResponseRedirect


class SupplierListView(ListView):
    context_object_name = 'supplier_list'
    model = Supplier


class SupplierDetailView(DetailView):
    model = Supplier

    def req_path(request):
        return request.path


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
