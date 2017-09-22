from django.db import models
from ..supplier.models import Supplier, Warehouse


class Product(models.Model):
    code = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.code)


class Match(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplier_code = models.CharField(max_length=15)

    def __str__(self):
        return self.supplier_code


class Quantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse,related_name='quantity', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now=True, auto_now_add=False)


    class Meta:
        unique_together = ('product', 'warehouse')


    def __str__(self):
        return str(self.product)


