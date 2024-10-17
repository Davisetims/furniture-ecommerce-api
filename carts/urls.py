from django.urls import path
from rest_framework.routers import DefaultRouter
from carts.views import CartViewSet

cart_router = DefaultRouter()

cart_router.register(r'carts', CartViewSet)

urlpatterns = [
    
]
urlpatterns  += cart_router.urls

