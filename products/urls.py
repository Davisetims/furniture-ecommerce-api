from django.urls import path
from rest_framework.routers import DefaultRouter
from products.views import CategoryViewSet, ProductViewSet
from . import views

product_router = DefaultRouter()
product_router.register(r'categories', CategoryViewSet)
product_router.register(r'products', ProductViewSet)

urlpatterns = [
    
    path(r'^media/(?P<path>.*\.obj)$', views.serve_3d_object),

]
urlpatterns += product_router.urls
