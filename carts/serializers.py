from rest_framework import serializers
from carts.models import Cart
from products.models import Product
from django.db import  transaction

class CartSerializer(serializers.ModelSerializer):
    items = serializers.JSONField()

    class Meta:
        model = Cart
        fields = ['id','customer', 'items', 'total_price', 'created_at']
        read_only_fields = ['total_price', 'created_at']

    def validate_items(self, items):
        # Ensure each item has 'product' and 'quantity' and validate stock levels
        for item in items:
            product_id = item.get('product')
            quantity = item.get('quantity')

            if not product_id or quantity is None:
                raise serializers.ValidationError("Each item must include 'product' and 'quantity'.")
            if quantity <= 0:
                raise serializers.ValidationError("Quantity must be greater than zero.")
            
            # Validate product existence and inventory level
            try:
                product = Product.objects.get(id=product_id)
                if product.product_inventory < quantity:
                    raise serializers.ValidationError(
                        f"Requested quantity for '{product.product_name}' exceeds available stock."
                    )
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist.")

        return items

    def create(self, validated_data):
        items = validated_data.pop('items', [])
        total_price = 0.0

        # Calculate total price and adjust inventory
        with transaction.atomic():
            for item in items:
                product_id = item['product']
                quantity = item['quantity']
                product = Product.objects.get(id=product_id)

                # Calculate item's total price and add to grand total
                item_total_price = product.product_price * quantity
                total_price += item_total_price

                # Adjust inventory for each product
                product.product_inventory -= quantity
                product.save()

            # Create the Cart instance with total price
            cart = Cart.objects.create(total_price=total_price, items=items, **validated_data)
        
        return cart