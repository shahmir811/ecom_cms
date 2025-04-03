from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse


class SuperuserRequiredView(LoginRequiredMixin, UserPassesTestMixin):
    """Base view that requires superuser status."""
    
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """Redirect the user to the previous page or login if not authenticated."""
        if not self.request.user.is_authenticated:
            messages.error(self.request, "You need to be logged in to access this page.")
            return redirect(reverse('users:login'))
        
        messages.error(self.request, "You don't have permission to access this page.")
        
        # Redirect to the previous page if available; otherwise, go to home.
        return redirect(self.request.META.get('HTTP_REFERER', reverse('users:home')))
