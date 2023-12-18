from django.db import models

# Create your models here.
class Wine(models.Model):
    name = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255)
    clubPrice = models.DecimalField(max_digits=10, decimal_places=2)
    listPrice = models.DecimalField(max_digits=10, decimal_places=2)
    salePrice = models.DecimalField(max_digits=10, decimal_places=2)
    productType = models.CharField(max_length=255)
    productSku = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name