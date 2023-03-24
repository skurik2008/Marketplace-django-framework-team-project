from .models import Review
from django import forms


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'rating', 'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 5})
        }
