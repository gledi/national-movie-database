from django import forms
from django.utils.translation import gettext as __
from django.utils.translation import gettext_lazy as _


class CartUpdateForm(forms.Form):
    quantity = forms.IntegerField(required=True, label=_("quantity"))

    def clean_quantity(self):
        qty = self.cleaned_data["quantity"]
        if qty == 0:
            raise forms.ValidationError(__("Useless to update quantity by 0"))
        return qty
