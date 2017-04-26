from apps.supplier.models import Email, Supplier
from django.forms import ModelForm, inlineformset_factory


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        exclude = ()


class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields= ['email', 'id', ]
        # exclude = ()


EmailFormSet = inlineformset_factory(Supplier, Email,
                                        form=EmailForm, can_delete=False, extra=2)