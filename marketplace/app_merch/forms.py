from django import forms

from .models import Offer, Review


class ReviewForm(forms.ModelForm):
    # seller = forms.ModelChoiceField(queryset=Seller.objects.all(), label='Продавец')

    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'rating', 'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 5})
        }


class PurchaseForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        offer = kwargs.pop('offer')
        super().__init__(*args, **kwargs)
        self.offer = offer
        self.fields['quantity'].max_value = offer.quantity

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity > self.offer.quantity:
            raise forms.ValidationError("Недостаточно товара для заказа.")
        return quantity
