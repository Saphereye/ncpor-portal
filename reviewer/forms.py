from django import forms
import authentication.models

class DeclineForm(forms.Form):
    alternate_reviewer_email = forms.ChoiceField(choices=[(i[0], i[0]) for i in authentication.models.Details.objects.filter(is_verifier = True).values_list('email')])

