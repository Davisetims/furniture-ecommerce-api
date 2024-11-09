from django.db import models, transaction
from django.core.exceptions import ValidationError
from users.models import User
from django.db.models import JSONField
from products.models import Product

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='cart_customer')
    items = JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Cart for {self.customer.username if self.customer else "Anonymous"}'

    def clean_items(self):
        """Validate items before saving"""
        if not isinstance(self.items, list):
            raise ValidationError("Items must be a list of product and quantity dictionaries.")

        for item in self.items:
            product_id = item.get('product')
            quantity = item.get('quantity')
            
            if not product_id or not quantity:
                raise ValidationError("Each item must have a 'product' and 'quantity' key.")

            if quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")

            product = Product.objects.filter(id=product_id).first()
            if not product:
                raise ValidationError(f"Product with ID {product_id} does not exist.")
            if product.product_inventory < quantity:
                raise ValidationError(
                    f"Requested quantity for '{product.product_name}' exceeds available stock."
                )

    def save(self, *args, **kwargs):
        self.clean_items()
        with transaction.atomic():
            for item in self.items:
                product_id = item['product']
                quantity = item['quantity']
                product = Product.objects.get(id=product_id)

                if product.product_inventory < quantity:
                    raise ValidationError(
                        f"Requested quantity for '{product.product_name}' exceeds available stock."
                    )

                # Deduct the quantity from product inventory
                product.product_inventory -= quantity
                product.save()

            super().save(*args, **kwargs)
            

class Payment(models.Model):
    PAYMENT_METHIOD_CHOICES = [
        ('cash', 'Cash'),
        ('mpesa', 'Mpesa'),
        
        
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHIOD_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    payment_status = models.CharField(max_length=10, choices= PAYMENT_STATUS_CHOICES, default='pending')
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, null=True, blank=True)