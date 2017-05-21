from .models import Email, Supplier
from django.forms import ModelForm, inlineformset_factory
from apps.supplier.models import Email, Supplier
from django.forms import ModelForm, inlineformset_factory, forms
from django.core.exceptions import ValidationError



class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        exclude = ()
    
    def clean(self):
        column_remain = self.cleaned_data.get('column_remain')
        column_code = self.cleaned_data.get('column_code')
        if column_remain == column_code:
            raise forms.ValidationError('Column remain and column code must be different')
        return self.cleaned_data


EmailFormSet = inlineformset_factory(Supplier,
                                     Email,
                                     fields=('email',),
                                     extra=2
                                     )


class MatchesUploadForm(forms.Form):
    matches = forms.FileField(label='Upload matches file:')
