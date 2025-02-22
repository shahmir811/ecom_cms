from django.db import models

from customers.models import Store

# Create your models here.
class Product(models.Model):
  store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
  name = models.CharField(max_length=500, null=True)
  asin = models.CharField(max_length=150, null=True)
  price = models.CharField(max_length=150, null=True)
  ratings = models.CharField(max_length=150, null=True)
  stars = models.CharField(max_length=150, null=True)
  brand = models.CharField(max_length=150, null=True)
  color = models.CharField(max_length=150, null=True)
  image_01 = models.CharField(max_length=150, null=True)
  image_02 = models.CharField(max_length=150, null=True)
  image_03 = models.CharField(max_length=150, null=True)


  description = models.TextField(null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True) 
  
  def __str__(self):
    return self.name
