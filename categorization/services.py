from django.db.models import QuerySet
from receipt_load.models import Product
from receipt_load.models import Category


def main():
    all_tags: dict = make_all_tags(Category.objects.all())
    for product in Product.objects.all():
        assign_category(product, all_tags)


def assign_category(product: Product, all_tags: dict):
    if product.category:
        return
    for tag in all_tags:
        if tag in product.name.lower():
            product.category = all_tags[tag]
            product.save()
            break


def make_all_tags(categories: QuerySet[Category]) -> dict:
    all_tags = dict()
    for category in categories:
        if not category.tags:
            continue
        category_tags = category.tags.split(', ')
        for tag in category_tags:
            all_tags[tag] = category
    return all_tags
