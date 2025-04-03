from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView
from django.views.generic.edit import FormView, UpdateView

from .forms import (CustomAuthenticationForm, UserProfileForm,
                    UserRegistrationForm)
from .mixins import SuperuserRequiredView
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


class UserListView(SuperuserRequiredView, ListView):
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

        messages.success(self.request, "Registration successful! You are now logged in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class UserProfileUpdateView(SuperuserRequiredView, UpdateView):
    model = Profile
    form_class = UserProfileForm
    template_name = 'users/update_profile.html'

    def get_object(self, queryset=None):
        """Ensure users can only edit their own profile."""
        return get_object_or_404(Profile, user_id=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request, "Profile updated successfully!")
        return reverse_lazy('users:list')

class AdminPasswordUpdateView(SuperuserRequiredView, UserPassesTestMixin, FormView):
    template_name = 'users/update_password.html'
    form_class = SetPasswordForm  # Using SetPasswordForm since old password isn't required
    success_url = reverse_lazy('users:list')

    def get_form_kwargs(self):
        """Pass the user instance to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_object()  # Ensure the form gets the correct user
        return kwargs

    def get_object(self, queryset=None):
        """Fetch the user whose password is being updated."""
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def test_func(self):
        """Allow only superusers to update another user's password."""
        return self.request.user.is_superuser

    def form_valid(self, form):
        """Set the new password and save the user."""
        user = self.get_object()
        form.save()  # Automatically sets the new password correctly
        messages.success(self.request, "User's password has been updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form errors."""
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class UserDeleteView(SuperuserRequiredView, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('users:list')

    def test_func(self):
        """Allow only superusers to delete users."""
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        """Show a success message when a user is deleted."""
        user = self.get_object()
        messages.success(request, f"User {user.username} has been deleted successfully.")
        return super().delete(request, *args, **kwargs)