from django.contrib import admin

from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'created')
    search_fields = ('user', 'name', 'email')

admin.site.register(Profile, ProfileAdmin)