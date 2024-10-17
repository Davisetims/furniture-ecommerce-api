from rest_framework import serializers
from carts.models import Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['customer', 'product', 'quantity', 'created_at']
    
    def validate(self, data):
        # Extract product and quantity from validated data
        product = data.get('product')
        quantity = data.get('quantity')
        
        # Check if quantity is zero
        if quantity == 0:
            raise serializers.ValidationError('Quantity cannot be zero.')
        
        # Check if product inventory is available
        if product.product_inventory == 0:
            raise serializers.ValidationError(f'The product "{product.product_name}" is out of stock.')
        
        # Ensure the quantity does not exceed available product inventory
        if quantity > product.product_inventory:
            raise serializers.ValidationError(f'The quantity ({quantity}) exceeds available stock ({product.product_inventory}).')
        
        return data


    def create(self, validated_data):
        # Adjust the inventory after validation and before saving
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        self.update_inventory(product, quantity)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Adjust the inventory during updates
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        self.update_inventory(product, quantity)
        return super().update(instance, validated_data)