from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from rest_framework.exceptions import NotFound
from users.models import User
from carts.models import Cart, Payment
from carts.serializers import CartSerializer, PaymentSerializer

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

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        customer= self.request.user
        if customer.is_superuser:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(customer=customer)
        
class GenerateInvoiceAPIView(APIView):
    """
    API View to generate and serve an invoice PDF.
    """

    def get(self, request, payment_id, *args, **kwargs):
        # Fetch the payment object
        try:
            payment = Payment.objects.select_related('customer', 'cart').get(id=payment_id)
        except Payment.DoesNotExist:
            raise NotFound(detail="Payment not found.")

        cart = payment.cart

        # Prepare context for the invoice
        context = {
            "customer_name": f"{payment.customer.first_name} {payment.customer.last_name}",
            "phone_number": getattr(payment.customer, "phone_number", "N/A"),
            "payment_method": payment.payment_method,
            "payment_date": payment.payment_date.strftime('%Y-%m-%d %H:%M:%S'),
            "amount_paid": payment.amount,
            "balance": 0,  # Replace with actual balance calculation logic if needed
            "payment_status": payment.payment_status,
            "cart_items": cart.items if cart else [],
        }

        # Render the invoice template to HTML
        html = render_to_string("invoice_template.html", context)

        # Generate the PDF response
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename=invoice_{payment.id}.pdf"

        # Convert HTML to PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return Response({"detail": "Error generating invoice PDF"}, status=500)

        return response