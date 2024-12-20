from django.contrib import admin
from carts.models import Cart, Payment

# class CartAdmin(admin.ModelAdmin):
#     list_display = ['cart_id', 'customer', 'items',  'created_at']
    
#     def cart_id(self,obj):
#         return obj.id
#     cart_id.short_description = 'cart_id'

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'customer_id', 'items', 'created_at']
    
    def cart_id(self, obj):
        return obj.id
    cart_id.short_description = 'cart_id'

    def customer_id(self, obj):
        return obj.customer.id if obj.customer else 'No Customer'
    customer_id.short_description = 'Customer_id'


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'customer_id', 'cart','payment_method', 'payment_date', 'payment_status', 'amount']
    
    def payment_id(self,obj):
        return obj.id
    payment_id.short_description = 'payment_id'

    def customer_id(self, obj):
        return obj.customer.id if obj.customer else 'No Customer'
    customer_id.short_description = 'Customer_id'
    
    
admin.site.register(Cart, CartAdmin)
admin.site.register(Payment,PaymentAdmin)