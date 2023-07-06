from django import forms
from .models import Details, Files


class DetailsForm(forms.ModelForm):
    class Meta:
        model = Details
        exclude = ("email", "proposal_number")


class FilesForm(forms.ModelForm):
    class Meta:
        model = Files
        exclude = ("email", "title_of_proposal",)
