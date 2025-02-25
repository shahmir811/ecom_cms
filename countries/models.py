from django.db import models

# Create your models here.
class Country(models.Model):
  name = models.CharField(max_length=500, null=True)
  code = models.CharField(max_length=50, null=True)
  website = models.CharField(max_length=150, null=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True) 
  
  def __str__(self):
    return self.name
