from django.db import models

from apps.product.models import Product
from apps.vendor.models import Vendor

# Create your models here.

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    vendors = models.ManyToManyField(Vendor, related_name='orders')

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return '%s' % self.id

    @property
    def get_total_price(self):
        return self.price * self.quantity  



