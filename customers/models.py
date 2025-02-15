from django.db import models

# Create your models here.
class Customer(models.Model):
  name = models.CharField(max_length=200, null=True)
  email = models.EmailField(max_length=500, null=True, unique=True)
  phone = models.CharField(max_length=100, null=True)
  address = models.CharField(max_length=200, null=True, blank=True)
  city = models.CharField(max_length=200, null=True, blank=True)
  state = models.CharField(max_length=200, null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.name
