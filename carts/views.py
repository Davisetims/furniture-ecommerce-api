from rest_framework import viewsets, permissions
from users.models import User
from carts.models import Cart
from carts.serializers import CartSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        customer= self.request.user
        if customer.is_superuser:
            return Cart.objects.all()
        else:
            return Cart.objects.filter(customer=customer)
        