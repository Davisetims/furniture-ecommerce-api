from django.db import models, transaction
from django.core.exceptions import ValidationError
from users.models import User
from django.db.models import JSONField
from products.models import Product

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='cart_customer')
    items = JSONField(null=True, blank=True)
    total_price = models.FloatField(editable=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Cart for {self.customer.username if self.customer else "Anonymous"}'

    def clean_items(self):
        """Validate items before saving."""
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
        grand_total = 0.0

        with transaction.atomic():
            for item in self.items:
                product_id = item['product']
                quantity = item['quantity']
                product = Product.objects.get(id=product_id)

                if product.product_inventory < quantity:
                    raise ValidationError(
                        f"Requested quantity for '{product.product_name}' exceeds available stock."
                    )

                # Calculate total for this product
                item_total = product.product_price * quantity
                item['total_price'] = item_total

                # Add to grand total
                grand_total += item_total

                # Deduct the quantity from product inventory
                product.product_inventory -= quantity
                product.save()

            # Set the cart's total price
            self.total_price = grand_total
            super().save(*args, **kwargs)