from django.urls import path
from rest_framework.routers import DefaultRouter
from carts.views import CartViewSet, GenerateInvoiceAPIView, PaymentViewSet

cart_router = DefaultRouter()

cart_router.register(r'carts', CartViewSet)
cart_router.register(r'payments',PaymentViewSet )

urlpatterns = [
    path('invoice/<int:payment_id>/', GenerateInvoiceAPIView.as_view(), name='generate_invoice'),
]

urlpatterns  += cart_router.urls

