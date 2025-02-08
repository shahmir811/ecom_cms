from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
  path("", views.StartingPageView.as_view(), name='starting-page'),
  path('home/', views.HomePageView.as_view(), name='home'),
  path('login/', views.CustomLoginFormView.as_view(), name='login'),
  path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]