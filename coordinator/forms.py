from django import forms
import authentication.models


class AssignedForm(forms.Form):
    proposal_number = forms.CharField(max_length=12)
    for i in range(5):
        exec(f"reviewer_{i+1}_email = forms.ChoiceField(choices=[('None', 'None')] + [(i[0], i[0]) for i in authentication.models.Details.objects.filter(is_verifier = True).values_list('email')])")
    