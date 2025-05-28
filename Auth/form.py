from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone_Number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise ValidationError("Passwords do not match")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username", required=True, widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))