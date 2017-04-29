from django.db import models

# Create your models here.


class Supplier(models.Model):
    name = models.CharField(max_length=30)
    column_remain = models.IntegerField()
    column_code = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.id


class Warehouse(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

    class Meta:
        unique_together = ('city', 'supplier')

    def __str__(self):
        return self.name


class Email(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    email = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.email










