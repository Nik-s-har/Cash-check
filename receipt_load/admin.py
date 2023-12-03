from django.contrib import admin
from .models import Category, Product, Retail, Purchase


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'category_verified']
    list_editable = ['category', 'category_verified']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'tags']
    list_editable = ['name', 'tags']


class RetailAdmin(admin.ModelAdmin):
    list_display = ['inn', 'name']
    ordering = ('name',)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_cost', 'receipt']


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Retail, RetailAdmin)
admin.site.register(Purchase, PurchaseAdmin)
