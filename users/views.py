from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

# Create your views here.

class StartingPageView(TemplateView):
    template_name = "users/starting_page.html"

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Your HTML login template
    redirect_authenticated_user = True  # Redirect if already logged in
    success_url = reverse_lazy('home')  # Redirect after successful login
    