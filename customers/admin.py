from django.contrib import admin

# Register your models here.
from .models import Customer, Store

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'city', 'created')
    search_fields = ('name', 'email', 'phone', 'city')

class StoreAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'created' )
    search_fields = ('owner', 'name')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Store, StoreAdmin)