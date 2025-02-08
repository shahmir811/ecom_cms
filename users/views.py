from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login 
from django.contrib import messages

from .forms import CustomAuthenticationForm 

class StartingPageView(TemplateView):
    template_name = "users/starting_page.html"

class HomePageView(TemplateView):
    template_name = "users/home.html"

class CustomLoginFormView(FormView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm  # Use the custom form
    success_url = reverse_lazy('users:home')

    def form_valid(self, form):
        """If the form is valid, log the user in and show success message."""
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'You have successfully logged in.')
        return super().form_valid(form)

    def form_invalid(self, form):
        """If authentication fails, show an error message."""
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view to add a success message."""
    next_page = reverse_lazy('users:starting-page')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)

