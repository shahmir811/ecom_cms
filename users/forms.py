from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
        label="Username",
        error_messages={
            'required': 'Username is required.',
            'invalid': 'Enter a valid username.',
        }
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        label="Password",
        error_messages={
            'required': 'Password field is required.',
            'invalid': 'Incorrect password, please try again.',
        }
    )
