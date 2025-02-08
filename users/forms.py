from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile

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


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
        label="Username",
        error_messages={
            'required': 'Username is required.',
            'invalid': 'Enter a valid username.',
        }
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
        label="Name",
        error_messages={
            'required': 'Name is required.',
        }
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        label="Email",
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
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

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "password"]
        labels = {
            'first_name': 'Name'
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")


class UserProfileForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
        label="Name",
        error_messages={'required': 'Name is required.'}
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        label="Email",
        error_messages={'required': 'Email is required.', 'invalid': 'Enter a valid email address.'}
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        label="Username",
        error_messages={'required': 'Username is required.'}
    )
    
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Profile Image"
    )
    
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'profile_image']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
            raise forms.ValidationError('This email is already in use by another account.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(username=self.instance.username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username
    
    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            if profile_image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Profile image size should not exceed 5MB.')
        return profile_image