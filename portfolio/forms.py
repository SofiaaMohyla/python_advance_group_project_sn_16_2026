from django import forms
from portfolio.models import Portfolio, Comments

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'media']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва портфоліо'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Опис портфоліо'}),
            'media': forms.FileInput(attrs={'class': 'form-control'})
        }
        
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content', 'media']
        
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Коментар'}),
            'media': forms.FileInput(attrs={'class': 'form-control'})
        }