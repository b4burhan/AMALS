from django import forms


class CartAddProductForm(forms.Form):
    """Form for adding products to cart"""
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control quantity-input',
            'min': '1'
        })
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )


class CartUpdateForm(forms.Form):
    """Form for updating cart quantity"""
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm text-center',
            'style': 'width: 60px;'
        })
    )
