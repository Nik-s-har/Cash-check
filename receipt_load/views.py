import json
from django.shortcuts import render
from django.views import View
from receipt_load.models import *



# Create your views here.

class ReceiptLoad(View):
    def get(self, request):
        return render(request, 'receipt_load/load_file.html')

    def post(self, request):
        reed_json(request.FILES['receipts'])
        return render(request, 'receipt_load/load_file.html')
def get_receopt_dict(receipt):
    try:
        return receipt['ticket']['document']['receipt']
    except KeyError:
        return receipt['ticket']['document']['bso']


def reed_json(file):
    receipts = json.load(file)
    for receipt in receipts: # Цикл по чекам из выгруженного файла
        receipt = get_receopt_dict(receipt)
        # Выполняем проверку на наличие чека в базе данных
        fiscal_document_number = receipt['fiscalDocumentNumber']
        if (not Receipt.objects.filter(fiscal_document_number=fiscal_document_number)):
            entering_data_in_Database(receipt)
    return None
list
def entering_data_in_Database(receipt):
    # Проверяем наличие магазина в БД, если отсутствует, созаем новую запись
    userInn = receipt['userInn']
    if Retail.objects.filter(inn=userInn):
        store = Retail.objects.get(inn=userInn)
    else:
        store = retail_create(receipt)
    # Заполняем таблицу receipt_load_store_receipt, содержащую реквизиты чека
    new_store_receipt = receipt_create(receipt, store)
    # Заполняем таблицу receipt_load_purchase, содержащую покупки в чеке
    purchase_create(receipt, new_store_receipt)
    return None

def retail_create(receipt):
    receipt_User = receipt['user']
    receipt_userInn = receipt['userInn']
    new_retail = Retail.objects.create(inn=receipt_userInn,
                                       name=receipt_User)
    return new_retail

def receipt_create(receipt, retail):  #функция записывает информацию о реквизитах чека
    receipt_fiscalDocumentNumber = receipt['fiscalDocumentNumber']
    receipt_dateTime = receipt['dateTime']
    receipt_fiscalDriveNumber = receipt['fiscalDriveNumber']
    receipt_fiscalSign = receipt['fiscalSign']
    receipt_totalSum = receipt['totalSum'] / 100
    receipt_itemsCount = len(receipt['items'])
    new_store_receipt = Receipt.objects.create(fiscal_document_number=receipt_fiscalDocumentNumber,
                                               date=receipt_dateTime,
                                               fiscal_drive_number=receipt_fiscalDriveNumber,
                                               fiscal_sign=receipt_fiscalSign,
                                               total_cost=receipt_totalSum,
                                               retail=retail,
                                               items_count=receipt_itemsCount)
    return new_store_receipt

def purchase_create(receipt, store_receipt): # Функция записывает информацию о покупках
    items = receipt['items']
    for item in items: # Цикл по покупкам внутри чека, заполняем базу данных покупок
        goods = item['name']
        # Проверяем наличие наименования товара в справочнике товаров
        if Product.objects.filter(name=goods):
            product_name = Product.objects.get(name=goods)
        else:
            product_name = products_create(item)
        item_quantity = item['quantity']
        item_price = item['price']
        item_price = item_price / 100
        item_sum = item['sum']
        item_sum = item_sum / 100
        Purchase.objects.create(name=product_name,
                                price=item_price,
                                quantity=item_quantity,
                                total_cost=item_sum,
                                receipt=store_receipt)
    return None

def products_create(item):
    item_name = item['name']
    new_product = Product.objects.create(name=item_name)
    return new_product

def mark_True_categoryVerified():
    new_products = Product.objects.filter(category_verified=False)
    for new_products_item in new_products:
        if new_products_item.category is not None:
            new_products_item.category_verified = True
            new_products_item.save()
    return None