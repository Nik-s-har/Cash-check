from django.db import models


# Create your models here.
class Retail(models.Model):
    inn = models.CharField(max_length=20)
    name = models.CharField(max_length=100)


class Receipt(models.Model):
    date = models.DateTimeField()
    fiscal_document_number = models.IntegerField()
    fiscal_drive_number = models.IntegerField()
    fiscal_sign = models.IntegerField()
    total_cost = models.FloatField()
    retail = models.ForeignKey(Retail, on_delete=models.PROTECT, null=True)


class Сategory(models.Model):
    name = models.CharField(max_length=100)
    tags = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Сategory, on_delete=models.PROTECT, null=True, blank=True)
    category_verified = models.BooleanField(default=False)


class Purchase(models.Model):
    name = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.FloatField()
    quantity = models.IntegerField()
    total_cost = models.FloatField()
    receipt = models.ForeignKey(Receipt, on_delete=models.deletion.RESTRICT)
