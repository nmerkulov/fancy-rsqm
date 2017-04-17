from django.db import models

# Create your models here.


class Warehouse(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=30)
    warehouse = models.ManyToManyField(Warehouse)

    def __str__(self):
        return self.name


class Email(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    email = models.CharField(max_length=30)

    def __str__(self):
        return self.email









