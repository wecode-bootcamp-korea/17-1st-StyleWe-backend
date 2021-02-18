from django.db import models
from django.db.models.deletion import PROTECT

FORBIDDEN = 1

class Order(models.Model):
    user                = models.ForeignKey('user.User', on_delete=models.CASCADE)
    price               = models.DecimalField(max_digits=15, decimal_places=3)
    orderer_name        = models.CharField(max_length=45)
    orderer_phone       = models.CharField(max_length=45)
    orderer_email       = models.CharField(max_length=2000) 
    delivery_name       = models.CharField(max_length=45)
    delivery_phone      = models.CharField(max_length=45)
    delivery_address    = models.CharField(max_length=500)

    class Meta:
        db_table = 'orders'

class Status(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'statuses'

class OrderedProduct(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    color_size  = models.ForeignKey('product.ColorSize', on_delete=models.PROTECT)
    status      = models.ForeignKey('Status', on_delete=models.PROTECT)
    order       = models.ForeignKey('Order', on_delete=models.SET_DEFAULT, default=FORBIDDEN)
    price       = models.DecimalField(max_digits=15, decimal_places=3)
    order_count = models.PositiveIntegerField(default=1)
    
    class Meta:
        db_table = 'ordered_products'
