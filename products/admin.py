from django.contrib import admin
from products.models import Category,Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'category_description')
    
    


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_category', 'product_name', 'product_description', 
                    'product_price', 'product_inventory', 'product_image', 'product_3D_object', 'created_at')

    def product_id(self, obj):
        return obj.id
    product_id.short_description = "product_id"  # This sets the verbose name for the column

admin.site.register(Product,ProductAdmin)
admin.site.register(Category, CategoryAdmin)