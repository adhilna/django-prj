from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'date_created')  # Columns to display in the admin list view
    search_fields = ('name', 'email')  # Fields to enable search functionality
    list_filter = ('date_created',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category') 
    search_fields = ('name', 'category')
    list_filter = ('date_created', 'category')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

