from django.db import models

# Create your models here.
class Retail(models.Model):
    retailInn = models.CharField(max_length=20)
    retailName = models.CharField(max_length=100)


class Store_receipt(models.Model):
    dateTime = models.DateTimeField()
    fiscalDocumentNumber = models.IntegerField()
    fiscalDriveNumber = models.IntegerField()
    fiscalSign = models.IntegerField()
    totalSum = models.FloatField()
    store = models.ForeignKey(Retail, on_delete=models.PROTECT, null=True)

class Product_category(models.Model):
    categoryName = models.CharField(max_length=100)
    keyWords = models.TextField(blank=True)

    def __str__(self):
        return f'{self.categoryName}'



class Products(models.Model):
    productName = models.CharField(max_length=100)
    category = models.ForeignKey(Product_category, on_delete=models.PROTECT, null=True, blank=True)
    categoryVerified = models.BooleanField(default=False)

class Purchase(models.Model):
    name = models.ForeignKey(Products, on_delete=models.PROTECT)
    price = models.FloatField()
    quantity = models.IntegerField()
    sum = models.FloatField()
    receipt = models.ForeignKey(Store_receipt, on_delete=models.deletion.RESTRICT)