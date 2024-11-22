from django.contrib import admin
from carts.models import Cart, Payment

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'items',  'created_at']
    
admin.site.register(Cart, CartAdmin)
admin.site.register(Payment)