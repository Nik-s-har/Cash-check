from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from receipt_load.models import Category
from statistics_output.servises.get_statistics import get_statistics, \
    itemization_month_category, get_year_statistics, get_vector_statistics
from statistics_output.servises.represent_statistics import statistics_as_table, purchases_as_table


def vector_statistics(request, year, month=None, parent_category="main", mode='simple'):
    year = int(year)
    month = int(month) if month else month

    if mode == "simple":
        statistics_table, total_cost = get_statistics(year, month, parent_category)
    elif mode == "vector":
        statistics_table, total_cost = get_vector_statistics(year, month, parent_category)

    date_url = f'/{year}/{month}/' if month else f'/{year}/'
    full_url = date_url if mode == 'simple' else f'/vector{date_url}'
    category_url = '' if parent_category == 'main' else f'/{parent_category}'
    mode_url = '' if mode == 'simpl' else f'/vector'
    change_mode_url = f'{category_url}/vector{full_url}' if mode == 'simple' else f'{category_url}{date_url}'
    try:
        back_category_name = Category.objects.get(name=parent_category).parent.name
    except:
        back_category_name = parent_category
    back_category_url = f'{full_url}' if back_category_name == 'main' else f'/{back_category_name}{full_url}'
    back_date_url = f'{category_url}{mode_url}/{year}/'
    header = statistics_table[0]
    del statistics_table[0]
    context = {'table_header': header,
               'table_content': statistics_table,
               'total_cost': total_cost,
               'full_url': full_url,
               'date_url': date_url,
               'category_url': category_url,
               'change_mode_url': change_mode_url,
               'back_category_url': back_category_url,
               'back_date_url': back_date_url,
               }
    return render(request, 'statistics_output/year_statistics_table.html', context)


def statistics(request, year, month=None, mode='simple', parent_category="main"):
    print(parent_category, year, month, mode)
    # return HttpResponse(f'parent_category: {parent_category}, mode: {mode}, year: {year}, month: {month}')
    statistics_table, total_cost = get_statistics(year, month, parent_category)
    date_url = f'{year}/{month}/' if month else f'/{year}/'
    context = {'statistics_table': statistics_table, 'total_cost': total_cost, 'date_url': date_url}
    return render(request, 'statistics_output/month_statistics_table.html', context)


def itemization(request, year, month, category):
    print(category)
    purchases, total_cost = itemization_month_category(year, month, category)
    purchases_table = purchases_as_table(purchases)
    context = {'purchases_table': purchases_table, 'total_cost': total_cost}
    return render(request, 'statistics_output/itemization_category_table.html', context)
