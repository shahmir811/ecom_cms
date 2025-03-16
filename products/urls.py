from django.urls import path

from .views import productDetails

app_name = 'products'


urlpatterns = [

  path('details/<int:product_id>/', productDetails, name='product-details'),
  
]