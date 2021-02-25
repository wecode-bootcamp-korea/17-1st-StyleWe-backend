from django.db import models
from django.db.models.deletion import PROTECT

class Order(models.Model):
    user                = models.ForeignKey('user.User', on_delete=models.CASCADE)
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
    user            = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    product_option  = models.ForeignKey('product.ProductOption', on_delete=models.PROTECT)
    status          = models.ForeignKey('Status', on_delete=models.PROTECT)
    order           = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    price           = models.DecimalField(max_digits=15, decimal_places=3)
    order_count     = models.PositiveIntegerField(default=1)
    in_cart_at      = models.DateTimeField(auto_now_add=True)
    purchased_at    = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'ordered_products'
