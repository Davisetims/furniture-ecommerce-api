from rest_framework import viewsets, permissions
from django.http import HttpResponse
from django.views.static import serve
from django.conf import settings
from products.models import Category,Product
from products.serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
def serve_3d_object(request, path):
    response = serve(request, path, document_root=settings.MEDIA_ROOT)
    response["Access-Control-Allow-Origin"] = "https://cessfuniture.netlify.app"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type"
    return response
    
