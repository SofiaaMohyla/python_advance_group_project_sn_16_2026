from django import forms
from django.forms import inlineformset_factory

from .models import Poll, PollOption


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ("title", "description", "is_active")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


PollOptionFormSet = inlineformset_factory(
    Poll,
    PollOption,
    fields=("text",),
    extra=2,
    min_num=2,
    validate_min=True,
    can_delete=True,
    widgets={"text": forms.TextInput(attrs={"class": "form-control"})},
)


class VoteForm(forms.Form):
    option = forms.ModelChoiceField(queryset=PollOption.objects.none(), widget=forms.RadioSelect)

    def __init__(self, *args, poll, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["option"].queryset = poll.options.all()
