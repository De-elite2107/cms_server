from django.contrib import admin
from .models import *
from django import forms

# Register your models here.
class ModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_superuser')  # Columns to display
    list_filter = ('is_active', 'is_superuser', 'is_staff', 'role')
    search_fields = ('username', 'email', 'role')

admin.site.register(User, ModelAdmin)