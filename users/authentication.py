from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    """Custom authentication backend to allow login with email instead of username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)  # Authenticate using email
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
