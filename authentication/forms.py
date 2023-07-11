from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser, Details
from phonenumber_field.modelfields import PhoneNumberField

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = CustomUser
		fields = ("email", "password1", "password2")

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class DetailsForm(forms.ModelForm):
    class Meta:
        model = Details
        exclude = ("email","is_pi", "is_verifier", "is_coordinator")
        