from django.urls import path
from .views import CustomersListView, CustomerCreateView, CustomerUpdateView


app_name = 'customers'

urlpatterns = [
    path('', CustomersListView.as_view(), name='list'),
    # path('add/', CustomerCreateView.as_view(), name='add'),
    path('create-customer/', CustomerCreateView.as_view(), name='create-customer'),
    path('update-customer/<int:pk>/', CustomerUpdateView.as_view(), name='update-customer'),  # New update route


    # path('edit/<int:pk>/', views.CustomerUpdateView.as_view(), name='edit'),
    # path('delete/<int:pk>/', views.CustomerDeleteView.as_view(), name='delete'),
    # path('detail/<int:pk>/', views.CustomerDetailView.as_view(), name='detail'),

]