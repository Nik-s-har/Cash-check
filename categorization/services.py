from django.db.models import QuerySet
from receipt_load.models import Products
from receipt_load.models import Product_category



def assign_category(product: Products, all_tags: dict):
    if product.category:
        return
    for tag in all_tags:
        if tag in product.productName.lower():
            product.category = all_tags[tag]
            product.save()
            break



def make_all_tags(categories: QuerySet[Product_category]):
    all_tags = dict()
    for category in categories:
        if not category.keyWords:
            continue
        category_tags = category.keyWords.split(', ')
        for tag in category_tags:
            all_tags[tag] = category
    return all_tags


def main():
    all_tags = make_all_tags(Product_category.objects.all())
    for product in Products.objects.all():
        assign_category(product, all_tags)


if __name__ == "__main__":
    all_tags = make_all_tags(Product_category.objects.all())
    for product in Products.objects.all():
        assign_category(product, all_tags)


