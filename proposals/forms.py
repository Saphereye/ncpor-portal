from django import forms
from .models import Details, Files


class DetailsForm(forms.ModelForm):
    class Meta:
        model = Details
        exclude = ()


class FilesForm(forms.ModelForm):
    class Meta:
        model = Files
        exclude = ("title_of_proposal",)
