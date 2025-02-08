from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import login 
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .forms import CustomAuthenticationForm, UserRegistrationForm, UserProfileForm
from .models import Profile

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


class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'


class UserRegistrationView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])  # Hash the password
        user.save()
        login(self.request, user)  # Log the user in
        messages.success(self.request, "Registration successful! You are now logged in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserProfileForm
    template_name = 'users/update_profile.html'

    def get_object(self, queryset=None):
        """Ensure users can only edit their own profile."""
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Profile updated successfully!")
        return reverse_lazy('users:list')