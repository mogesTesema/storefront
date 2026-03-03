from django.shortcuts import render
import requests
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
from django.views.decorators.csrf import csrf_exempt
import logging
import os

logger = logging.getLogger(__name__)

@cache_page(2*60)
def say_hello(request):
   
    pass


class SayHelloView(APIView):

    @method_decorator(cache_page(5*60))
    def get(self,request):
        logger.info("slow endpoint called")
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        logger.critical('slow endpoint done')
        return render(request,'hello.html',{'name':data})






CHAPA_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_SECRET_KEY = os.environ.get("CHAPA_SECRET_KEY")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment(request):
    """
    Initialize payment with Chapa
    """
    serializer = PaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    payment = serializer.save(
    user=request.user,
    status="pending"
)

    

    headers = {
        "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "amount": str(payment.amount),
        "currency": payment.currency,
        "email": payment.user.email,
        "first_name": payment.user.first_name or "Customer",
        "last_name": payment.user.last_name or "User",
        "tx_ref": str(payment.tx_ref),
        "callback_url": "https://subarcuated-jani-unimmanently.ngrok-free.dev/playground/webhook/",
        "return_url": "https://subarcuated-jani-unimmanently.ngrok-free.dev/playground/payment-success/",
        "customization": {
            "title": "Payment for App",
            "description": "Order payment"
        }
    }

    try:
        chapa_response = requests.post(
            CHAPA_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        chapa_response_data = chapa_response.json()

        if chapa_response.status_code != 200:
            payment.status = "failed"
            payment.save()

            return Response(
                {"error": "Failed to initialize payment", "details": chapa_response_data},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": "Payment initialized successfully",
            "checkout_url": chapa_response_data["data"]["checkout_url"],
            "tx_ref": payment.tx_ref
        })

    except requests.exceptions.RequestException as e:
        payment.status = "failed"
        payment.save()

        return Response(
            {"error": "Connection error", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )








VERIFY_URL = "https://api.chapa.co/v1/transaction/verify/"

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def chapa_webhook(request):
    tx_ref = request.data.get("tx_ref")

    if not tx_ref:
        return Response({"error": "tx_ref missing"}, status=400)

    try:
        payment = Payment.objects.get(tx_ref=tx_ref)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)



    headers = {
        "Authorization": f"Bearer {CHAPA_SECRET_KEY}"
    }


    verify_response = requests.get(
        f"{VERIFY_URL}{tx_ref}",
        headers=headers
    )

    verify_data = verify_response.json()

    if verify_response.status_code == 200 and verify_data["data"]["status"] == "success":
        payment.status = "success"
    else:
        payment.status = "failed"

    payment.save()

    print("\n"*10)
    print(payment.status)
    print("\n"*5)

    return Response({"message": "Webhook processed","status":payment.status})



class PaymentSuccessView(APIView):
    def get(self, request):
        tx_ref = request.query_params.get("tx_ref", "")
        context = {"message": "Payment completed successfully.", "tx_ref": tx_ref}
       
        return render(request, "payment_success.html", context)