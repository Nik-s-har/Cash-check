from operator import itemgetter

def statistics_as_table(statistics):
    table = []
    for category in statistics:
        line = [category,
                statistics[category].quantity,
                round(statistics[category].cost),
                round(statistics[category].share_in_total_cost, 1)]
        table += [line]
    table = sorted(table, key=itemgetter(3), reverse=True)
    return table


def purchases_as_table(purchases):
    table = []
    for purchase in purchases:
        line = [purchase.name.name,
                round(purchase.price),
                purchase.quantity,
                round(purchase.total_cost)]
        table += [line]
    table = sorted(table, key=itemgetter(3), reverse=True)
    return table