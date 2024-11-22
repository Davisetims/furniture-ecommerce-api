from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('furniture_store_owner', 'Furniture Store Owner'),
        
    ]
    first_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='user_first_name')
    last_name = models.CharField(max_length=40, null=True,blank=True, verbose_name='user_last_name')
    username = models.CharField(max_length=40, unique=True,null=True, blank=True, verbose_name='user_username')
    phone_number = models.CharField(max_length=15, null=True,blank=True,verbose_name='user_phone_number')
    address = models.CharField(max_length=255, null=True, blank=True,verbose_name='user_address')
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name='user_email')
    national_id = models.PositiveIntegerField(null=True,blank=True,verbose_name='user_national_id')
    password = models.CharField(max_length= 1000, null=True, blank=True, verbose_name='user_password')
    user_type = models.CharField(max_length=30, choices= USER_TYPE_CHOICES, default='customer')  
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.username