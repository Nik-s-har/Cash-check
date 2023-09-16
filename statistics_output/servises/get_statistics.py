from datetime import date, timedelta
from django.db.models import QuerySet
from recordtype import recordtype
from receipt_load.models import Purchase
from receipt_load.models import Category
from receipt_load.models import Product
from receipt_load.models import Receipt

CategoryStatistics = recordtype(
    'CategoryStatistics', ['cost',
                           'share_in_total_cost']
)


class HierarchyTree:
    def __init__(self, categories: QuerySet[Category]):
        tree = dict()
        for category in categories:
            if not category in tree:
                tree[category] = set()
            if not category.parent is None and not category.parent in tree:
                tree[category.parent] = {category}
            if not category.parent is None and category.parent in tree:
                tree[category.parent].add(category)
        self.tree = tree

    def products_by_category(self, category_name):
        def fill_atom_sub_categories(tree, category_name, atom_sub_categories):
            category = Category.objects.get(name=category_name)
            if not tree[category]:
                atom_sub_categories.append(category)
                return
            for child in tree[category]:
                fill_atom_sub_categories(tree, child.name, atom_sub_categories)

        atom_sub_categories = []
        tree = self.tree
        fill_atom_sub_categories(tree, category_name, atom_sub_categories)

        products_by_category = []

        for sub_category in atom_sub_categories:
            products_by_sub_category = list(Product.objects.filter(category=sub_category))
            products_by_category += products_by_sub_category

        return products_by_category


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


def get_period(year: int, month: int | None):
    if month:
        end = (date(year, month + 1, 1) + timedelta(days=-1)).day
    else:
        end = 12
    return [i for i in range(1, end + 1)]

def get_period_date(date, period_time):
    if date[1]:
        date.append(period_time)
    else:
        date[1] = period_time
        date.append(None)
    return date

def get_vector_statistics(year: int, month: int | None, parent_category: str):
    # purchases = filter_by_date(Purchase.objects.all(), year, month)
    period = get_period(year, month)
    table = [['category'] + [i for i in period] + ['total_cost', 'share']]

    parent_category = Category.objects.get(name=parent_category)
    categories = Category.objects.all()
    hierarchy = HierarchyTree(categories)
    sub_categories = hierarchy.tree[parent_category]

    total_cost = 0
    for sub_category in sub_categories:
        line_in_table = [sub_category.name]
        total_cost_category = 0
        for period_time in period:
            period_date = get_period_date([year, month], period_time)
            purchases = filter_by_date(Purchase.objects.all(), period_date)
            time_cost = get_cost_by_category(purchases, sub_category, hierarchy)
            line_in_table.append(time_cost)
            total_cost_category += time_cost
        total_cost += total_cost_category
        line_in_table.append(total_cost_category)
        table.append(line_in_table)

    add_share_in_total_cost(table, total_cost)

    return table, total_cost


def get_statistics(year: int, month: int | None, parent_category: str, day=None):
    statistics: dict[str: CategoryStatistics] = {}
    purchases = filter_by_date(Purchase.objects.all(), [year, month, day])
    if not purchases:
        return None

    table = [['category', 'total_cost', 'share']]
    parent_category = Category.objects.get(name=parent_category)
    categories = Category.objects.all()
    hierarchy = HierarchyTree(categories)
    sub_categories = hierarchy.tree[parent_category]

    total_cost = 0
    for sub_category in sub_categories:
        category_cost = get_cost_by_category(purchases, sub_category, hierarchy)
        total_cost += category_cost
        line_in_table = [sub_category.name, category_cost]
        table.append(line_in_table)

    add_share_in_total_cost(table, total_cost)
    print(table)
    return table, total_cost


def itemization_month_category(year, month, category):
    purchases = filter_by_date(Purchase.objects.all(), year, month)
    category = Category.objects.get(name=category)
    purchases = filter_by_category(purchases, category)
    total_cost = get_total_cost(purchases)
    return purchases, round(total_cost)


def get_cost_by_category(purchases, category, hierarchy):
    purchases = filter_by_category(purchases, category, hierarchy)
    cost = get_total_cost(purchases)
    return cost


def add_share_in_total_cost(table, total_cost):
    for i in range(1, len(table)):
        print(table[i])
        table[i].append(f"{round((table[i][-1] / total_cost) * 100, 2)} %")
        print(table[i])

def get_total_cost(purchases):
    total_cost = 0
    for purchase in purchases:
        total_cost += purchase.total_cost
    return total_cost


def filter_by_category(purchases, category, hierarchy):
    product_by_category = hierarchy.products_by_category(category.name)
    purchases_by_category = purchases.filter(name__in=product_by_category)
    return purchases_by_category


def filter_by_date(purchases, our_date: list):
    date_period = calculate_date_period(our_date)
    receipt_month = Receipt.objects.filter(date__range=date_period)
    purchases_month = purchases.filter(receipt__in=receipt_month)
    return purchases_month


def calculate_date_period(our_date: list):
    if our_date[2]:
        start = date(our_date[0], our_date[1], our_date[2])
        end = start + timedelta(days=1)
    elif our_date[1] == 12:
        start = date(our_date[0], our_date[1], 1)
        end = date(our_date[0] + 1, 1, 1) + timedelta(days=-1)
    elif our_date[1]:
        start = date(our_date[0], our_date[1], 1)
        end = date(our_date[0], our_date[1] + 1, 1) + timedelta(days=-1)
    else:
        start = date(our_date[0], 1, 1)
        end = date(our_date[0], 12, 31)
    return [start, end]
