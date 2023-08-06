from django import forms

from calender.models import Register


class RegisterUpdateForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ["user", "event", "is_present"]
        widgets = {"user": forms.HiddenInput, "event": forms.HiddenInput}
        labels = {"is_present": "I will be there"}
