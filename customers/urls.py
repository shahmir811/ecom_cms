from django.urls import path
from .views import CustomersListView, CustomerCreateView, CustomerDetailsView, CustomerUpdateView, StoresListView, StoreCreateView, StoreDetailsView, StoreUpdateView


app_name = 'customers'

urlpatterns = [
    path('', CustomersListView.as_view(), name='list'),
    # path('add/', CustomerCreateView.as_view(), name='add'),
    path('create-customer/', CustomerCreateView.as_view(), name='create-customer'),
    path('view-customer/<int:pk>/', CustomerDetailsView.as_view(), name='view-customer'),
    path('update-customer/<int:pk>/', CustomerUpdateView.as_view(), name='update-customer'),


    path('stores/', StoresListView.as_view(), name='stores_list'),
    path('create-store/', StoreCreateView.as_view(), name='stores_create'),
    path('view-store/<int:pk>/', StoreDetailsView.as_view(), name='stores_view'),
    path('update-store/<int:pk>/', StoreUpdateView.as_view(), name='stores_update'),


    # path('delete/<int:pk>/', views.CustomerDeleteView.as_view(), name='delete'),
    # path('detail/<int:pk>/', views.CustomerDetailView.as_view(), name='detail'),

]