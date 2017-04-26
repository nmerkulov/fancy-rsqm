from django.shortcuts import render, redirect
from apps.supplier.models import Supplier, Email
from django.views.generic import ListView, DetailView
from apps.supplier.forms import SupplierForm, EmailFormSet, EmailForm
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory


class SupplierListView(ListView):
    context_object_name = 'supplier_list'
    model = Supplier


class SupplierDetailView(DetailView):
    model = Supplier
    def req_path(request):
        print (request.path)
        return request.path


def add_supplier_card(request):
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)
        email_formset = EmailFormSet(request.POST or None, prefix='emails')
        if supplier_form.is_valid() and email_formset.is_valid():
            name = supplier_form.cleaned_data['name']
            column_remain = supplier_form.cleaned_data['column_remain']
            column_code = supplier_form.cleaned_data['column_code']
            new_sup = Supplier.objects.create(
                            name=name,
                            column_remain=column_remain,
                            column_code=column_code,
                                    )
            new_sup.save()
            for dicts in email_formset.cleaned_data:
                if len(dicts) > 0:
                    new_email = Email.objects.create(
                                    supplier_id=new_sup.id, 
                                    email=dicts['email']
                                        )
                    new_email.save()
            return HttpResponseRedirect('/supplier/')
    else:
        supplier_form = SupplierForm()
        email_formset = EmailFormSet(prefix='emails')
    return render(request, 'create_card.html', {
        'supplier_form': supplier_form,
        'email_formset': email_formset,
        })


def edit_supplier_card(request, s_id):
    instance = Supplier.objects.get(id=s_id)
    email_list = list(instance.email_set.all())
    EmailFormSet2 = inlineformset_factory(Supplier, Email,
                                          form=EmailForm, extra=2)
    if len(email_list) == 1:
        initials = [{'email': email_list[0].email, 'id': email_list[0].id}]
    elif len(email_list) > 1:
        initials = [{'email': email_list[0].email,
                     'id': email_list[0].id},
                    {'email': email_list[1].email,
                     'id': email_list[1].id}]
    else:
        initials = None
    supplier_form = SupplierForm(request.POST or None, instance=instance)
    formset = EmailFormSet2(request.POST or None, initial=initials)
    if supplier_form.is_valid() and formset.is_valid():
        instance = supplier_form.save(commit=False)
        instance.save()
        for dict in formset.cleaned_data:
            print(formset.cleaned_data)
            if len(dict) > 0:
                if dict['DELETE'] == True:
                    obj = Email.objects.get(id=dict['id'].id)
                    obj.delete()
                elif dict['id'] == None:
                    new_email = Email.objects.create(
                                    supplier_id=instance.id,
                                    email=dict['email']
                                        )
                    new_email.save()
                else:
                    obj.email = dict['email']
                    obj.save()
        return HttpResponseRedirect('/supplier/')
    context = {
        'supplier_form': supplier_form,
        'instance': instance,
        'formset': formset
        }
    return render(request, 'edit_card.html', context)

def delete_supplier_card(request, s_id):
    instance = Supplier.objects.get(id=s_id)
    instance.delete()
    return redirect('sup_list')