from django.contrib import admin

# Register your models here.
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'city', 'created')
    search_fields = ('name', 'email', 'phone', 'city')


admin.site.register(Customer, CustomerAdmin)