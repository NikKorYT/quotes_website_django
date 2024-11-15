from django import forms
from .models import Author, Quote, Tag

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['full_name', 'born_date', 'born_location', 'description']
        widgets = {
            'born_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 5, 'class': 'form-control'}
            )
        }

class QuoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'tag-select-multiple',
            }
        ),
        required=False
    )
    
    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']
        widgets = {
            'quote': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
            'author': forms.Select(
                attrs={'class': 'form-control'}
            )
        }

    def clean_quote(self):
        quote = self.cleaned_data['quote']
        if not quote.startswith('"'):
            quote = f'"{quote}'
        if not quote.endswith('"'):
            quote = f'{quote}"'
        return quote