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
    }