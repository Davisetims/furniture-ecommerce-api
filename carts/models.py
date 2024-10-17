from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
from products.models import Product

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'customer: {self.customer.username}, product: {self.product.product_name}'
    
    def save(self, *args, **kwargs):
        if self.quantity == 0:
            raise ValidationError('Quantity cannot be zero.')
        if self.product.product_inventory == 0:
            raise ValidationError(f'The product "{self.product.product_name}" is out of stock.')
        
        if self.quantity > self.product.product_inventory:
            raise ValidationError(f'The quantity ({self.quantity}) exceeds available stock ({self.product.product_inventory}).')
 
        self.product.product_inventory -= self.quantity
        self.product.save()
        
        super().save(*args, **kwargs)

