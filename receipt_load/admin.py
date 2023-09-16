from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'category_verified']
    list_editable = ['category', 'category_verified']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'tags']
    list_editable = ['name', 'tags']


# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
