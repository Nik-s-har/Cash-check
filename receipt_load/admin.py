from django.contrib import admin
from .models import Product_category, Products

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['productName', 'category', 'categoryVerified']
    list_editable = ['category', 'categoryVerified']

class Product_categoryAdmin(admin.ModelAdmin):
    list_display = ['categoryName', 'keyWords']
    list_editable = ['categoryName', 'keyWords']

# Register your models here.
admin.site.register(Product_category)
admin.site.register(Products, ProductsAdmin)