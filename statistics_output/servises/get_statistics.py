from recordtype import recordtype
from receipt_load.models import Purchase
from receipt_load.models import Сategory
from receipt_load.models import Product
from receipt_load.models import Receipt

CategoryStatistics = recordtype(
    'CategoryStatistics', ['quantity',
                           'cost',
                           'share_in_total_cost']
)

def get_year_statistics(year):
    year_statistics = []
    year_total_cost = 0
    purchases = Purchase.objects.all()
    for month in range(1, 13):
        month_purchases = filter_by_date(purchases, year, month)
        month_total_cost = round(get_total_cost(month_purchases))
        year_statistics.append(month_total_cost)
        year_total_cost += month_total_cost
    return year_statistics, year_total_cost


def get_month_statistics(year, month):
    statistics: dict[str: CategoryStatistics] = {}
    purchases = filter_by_date(Purchase.objects.all(), year, month)
    if not purchases:
        return None
    for category in Сategory.objects.all():
        category_statistics = get_statistics_by_category(purchases, category)
        statistics[category.name] = category_statistics
    total_cost = get_total_cost(purchases)
    calculate_share_in_total_cost(statistics, total_cost)
    return statistics, round(total_cost)


def itemization_month_category(year, month, category):
    purchases = filter_by_date(Purchase.objects.all(), year, month)
    category = Сategory.objects.get(name=category)
    purchases = filter_by_category(purchases, category)
    total_cost = get_total_cost(purchases)
    return purchases, round(total_cost)


def get_statistics_by_category(purchases, category):
    purchases = filter_by_category(purchases, category)
    quantity = get_total_quantity(purchases)
    cost = get_total_cost(purchases)
    return CategoryStatistics(quantity, cost, None)


def calculate_share_in_total_cost(statistics, total_cost):
    for category in statistics.values():
        category.share_in_total_cost = (category.cost / total_cost) * 100


def get_total_cost(purchases):
    total_cost = 0
    for purchase in purchases:
        total_cost += purchase.total_cost
    return total_cost


def get_total_quantity(purchases):
    total_quantity = 0
    for purchase in purchases:
        total_quantity += purchase.quantity
    return total_quantity


def filter_by_category(purchases, category):
    name_by_category = Product.objects.filter(category=category)
    purchases_by_category = purchases.filter(name__in=name_by_category)
    return purchases_by_category


def filter_by_date(purchases, year, month):
    receipt_month = Receipt.objects.filter(
        date__year=year,
        date__month=month)
    purchases_month = purchases.filter(receipt__in=receipt_month)
    return purchases_month
