from django import forms
from events.models import Event

class EventForm(forms.ModelForm):
  class Meta:
    model = Event
    fields = ['title', 'description', 'date', 'creator']

    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'description': forms.Textarea(attrs={'class': 'form-control'}),
      'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
      'type': forms.Select(attrs={'class': 'form-control'}),
      'place': forms.TextInput(attrs={'class': 'form-control'}),
    }


class EventFilterForm(forms.Form):
  type = forms.ChoiceField(choices=[("", "Всі")] + Event.TYPE_CHOICES, label='Тип події',required=False, widget=forms.Select(attrs={'class': 'form-control'}))

  class Meta:
    widgets = {
      'ензу': forms.Select(attrs={'class': 'form-control', 'required': False}),
    }