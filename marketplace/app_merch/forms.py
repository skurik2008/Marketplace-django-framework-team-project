from app_users.models import Seller
from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    # seller = forms.ChoiceField(choices=[], label='Продавец')
    seller = forms.ModelChoiceField(queryset=Seller.objects.all(), label='Продавец')

    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'rating', 'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 5})
        }


