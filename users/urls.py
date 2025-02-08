from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
  path("", views.StartingPageView.as_view(), name='starting-page'),
  path('login/', CustomLoginView.as_view(), name='login'),
]