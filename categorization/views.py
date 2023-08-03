from django.shortcuts import render
from receipt_load.models import Product, Сategory

# Create your views here.


def assing_category():
    products_without_category = Product.objects.filter(category=None)
    categories = Сategory.objects.all()
    for product in products_without_category:
        found_category = find_category(product, categories)
        if found_category:
            product.category = found_category
            product.save()
    pass

def find_category(product, categories):
    product_name = prduct.name
    found_category = None
    for category in categories:
        if find_keywords(product_name, category):
            found_category = category
            break
    return found_category

def find_keywords(product_name, category):
    return resalt
