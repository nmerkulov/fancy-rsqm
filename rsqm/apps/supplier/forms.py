from apps.supplier.models import Email, Supplier
from django.forms import ModelForm, inlineformset_factory


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        exclude = ()


EmailFormSet = inlineformset_factory(Supplier,
                                     Email,
                                     fields=('email',),
                                     extra=2
                                     )
