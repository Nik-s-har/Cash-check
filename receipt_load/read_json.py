import json

from receipt_load.models import Receipt, Retail, Product, Purchase

BANK = Retail.objects.get(name='ЦЕНТРАЛЬНЫЙ БАНК РОССИЙСКОЙ ФЕДЕРАЦИИ')
BANK_DINNER = Product.objects.get(name='обед')


def reed_json(file):
    input_data = json.load(file)
    for record in get_records(input_data):
        create_retail(record)
        create_receipt(record)
        create_products(record)
        create_purchases(record)


def create_retail(record):
    try:
        Retail.objects.get(inn=record['userInn'])
    except Retail.DoesNotExist:
        Retail.objects.create(inn=record['userInn'], name=record['user'])


def create_receipt(record):
    Receipt.objects.create(
        fiscal_document_number=record['fiscalDocumentNumber'],
        date=record['dateTime'],
        fiscal_drive_number=record['fiscalDriveNumber'],
        fiscal_sign=record['fiscalSign'],
        total_cost=get_number(record['totalSum']),
        retail=Retail.objects.get(inn=record['userInn']),
        items_count=len(record['items']),
    )


def create_products(record):
    if record['user'] == BANK.name:
        return

    for item in record['items']:
        try:
            Product.objects.get(name=item['name'])
        except Product.DoesNotExist:
            Product.objects.create(name=item['name'])


def create_purchases(record):
    if record['user'] == BANK.name:
        create_bank_purchases(record)
        return

    for item in record['items']:
        Purchase.objects.create(
            name=Product.objects.get(name=item['name']),
            price=get_number(item['price']),
            quantity=item['quantity'],
            total_cost=get_number(item['sum']),
            receipt=Receipt.objects.get(fiscal_document_number=record['fiscalDocumentNumber']),
        )


def create_bank_purchases(record):
    total_cost = 0
    for item in record['items']:
        total_cost += get_number(item['sum'])

    Purchase.objects.create(
        name=BANK_DINNER,
        price=total_cost,
        quantity=1,
        total_cost=total_cost,
        receipt=Receipt.objects.get(fiscal_document_number=record['fiscalDocumentNumber']),
    )


def get_records(input_data):
    '''возвращает только те рекорды, которые не были обработанны ранее.'''

    for frame in input_data:
        try:
            record = frame['ticket']['document']['receipt']
        except KeyError:
            record = frame['ticket']['document']['bso']

        try:
            Receipt.objects.get(fiscal_document_number=record['fiscalDocumentNumber'])
        except Receipt.DoesNotExist:
            yield record


def get_number(input_data_number):
    return input_data_number / 100
