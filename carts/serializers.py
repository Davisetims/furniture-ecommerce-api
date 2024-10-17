from rest_framework import serializers
from carts.models import Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['customer', 'product', 'quantity', 'created_at']
    
    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')
        
        if quantity == 0:
            raise serializers.ValidationError('Quantity cannot be zero.')

        
        if product.product_inventory == 0:
            raise serializers.ValidationError(f'The product "{product.product_name}" is out of stock.')
        
        if quantity > product.product_inventory:
            raise serializers.ValidationError(f'The quantity ({quantity}) exceeds available stock ({product.product_inventory}).')
        
        return data
    
    def create(self, validated_data):
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        return super().update(instance, validated_data)