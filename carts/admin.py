from django.contrib import admin
from carts.models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'items', 'total_price', 'created_at']
    
admin.site.register(Cart, CartAdmin)