from django import forms
from .material import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'description', 'image', 'file', 'you_tube_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'you_tube_link': forms.URLInput(attrs={'class': 'form-control'}),
        }