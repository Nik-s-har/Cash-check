from django.shortcuts import render
from statistics_output.servises.get_statistics import get_month_statistics, \
    itemization_month_category, get_year_statistics
from statistics_output.servises.represent_statistics import statistics_as_table, purchases_as_table


def year_statistics(request, year):
    statistics_table, total_cost = get_year_statistics(year)
    print(statistics_table, total_cost)
    months = [1, 2, 3, 4 ,5 ,6, 7, 8, 9, 10, 11, 12]
    context = {'months': months, 'statistics_table': statistics_table, 'total_cost': total_cost}
    return render(request, 'statistics_output/year_statistics_table.html', context)

def month_statistics(request, year, month):
    statistics, total_cost = get_month_statistics(year, month)
    statistics_table = statistics_as_table(statistics)
    context = {'statistics_table': statistics_table, 'total_cost': total_cost}
    return render(request, 'statistics_output/month_statistics_table.html', context)


def itemization(request, year, month, category):
    print(category)
    purchases, total_cost = itemization_month_category(year, month, category)
    purchases_table = purchases_as_table(purchases)
    context = {'purchases_table': purchases_table, 'total_cost': total_cost}
    return render(request, 'statistics_output/itemization_category_table.html', context)
