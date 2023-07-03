from django import forms

class MainForm(forms.Form):
    date_low = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_high = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
