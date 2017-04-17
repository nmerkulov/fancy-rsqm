from django.db import models

# Create your models here.


class Email(models.Model):
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.email


class Warehouse(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=30)
    warehouse = models.ManyToManyField(Warehouse)
    email = models.ForeignKey(Email)

    def __str__(self):
        return self.name



