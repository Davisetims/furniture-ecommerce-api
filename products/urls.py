from django.urls import path
from rest_framework.routers import DefaultRouter
from products.views import CategoryViewSet, ProductViewSet

product_router = DefaultRouter()
product_router.register(r'categories', CategoryViewSet)
product_router.register(r'products', ProductViewSet)

urlpatterns = [
    
]
urlpatterns += product_router.urls
