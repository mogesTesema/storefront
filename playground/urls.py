from django.urls import path
from . import views

# URLconf
urlpatterns = [
    path("hello/",views.SayHelloView.as_view()),
    path("payment/",views.payment),
    path("webhook/", views.chapa_webhook),
    path("payment-success/", views.PaymentSuccessView.as_view(), name="payment-success"),
]
