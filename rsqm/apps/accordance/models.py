from django.db import models
from apps.supplier.models import Supplier, Warehouse


class Product(models.Model):
    code = models.IntegerField()


class Match(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplier_code = models.CharField(max_length=15)

    def __str__(self):
        return self.suplier_code


class Quantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()





