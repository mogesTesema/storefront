from django.urls import path
from . import views

# URLconf
urlpatterns = [
    path("hello/",views.SayHelloView.as_view())
]
