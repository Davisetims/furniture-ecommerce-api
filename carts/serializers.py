from rest_framework import serializers
from carts.models import Cart

class CartSerializer(serializers.ModelSerializer):
    items = serializers.JSONField()

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'items', 'created_at']

    def validate_items(self, items):
        # Ensure each item has 'product' and 'quantity'
        for item in items:
            if 'product' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item must include 'product' and 'quantity'.")
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than zero.")
        return items

    def create(self, validated_data):
        return Cart.objects.create(**validated_data)
    
