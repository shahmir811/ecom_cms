from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
  path("", views.StartingPageView.as_view(), name='starting-page'),
  path('login/', views.CustomLoginFormView.as_view(), name='login'),
  path('logout/', views.CustomLogoutView.as_view(), name='logout'),
  path('register/', views.UserRegistrationView.as_view(), name='register'),

  path('users/', views.UserListView.as_view(), name='list'),
  path('home/', views.HomePageView.as_view(), name='home'),
  path('users/update-profile/<int:pk>/', views.UserProfileUpdateView.as_view(), name='update-profile'),

]