from django.db import models

class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('living_room_furniture', 'Living Room Furniture'),
        ('bedroom_furniture', 'Bedroom Furniture'),
        ('kitchen_furniture', 'Kitchen Furniture'),
        ('dining_room_furniture','Dining Room Furniture'),
        ('outdoor_furniture', 'Outdoor Furniture'),
        ('office_furniture', 'Office Furniture'),
        ('bathroom_furniture','Bathroom Furniture'),
        ('kids_furniture', 'Kids Furniture'),
        ('entryway_furniture','Entryway Furniture')
        
    ]
    category_name = models.CharField(max_length=60,choices=CATEGORY_TYPE_CHOICES, null=True, blank=True)
    category_description  = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.category_name
    
    
class Product(models.Model):
    product_name = models.CharField(max_length=50, null=True, blank=True)
    product_description = models.TextField(null=True, blank=True)
    product_price = models.FloatField(null=True, blank=True)
    product_inventory = models.IntegerField(null=True, blank=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    product_image  = models.ImageField(upload_to='product_images/',null=True,blank=True)
    product_3D_object = models.FileField(upload_to='product_3d_models/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product_name}, amount: {self.product_price}"
    
    
    
    