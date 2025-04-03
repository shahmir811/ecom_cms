from django.urls import path

from .views import ProductsListView, productDetails

app_name = 'products'


urlpatterns = [

  path('details/<int:product_id>/', productDetails, name='product-details'),
  path('list/', ProductsListView.as_view(), name='products-list'),
  
]