from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# it is request-handle, action, the name view is so confusing.
def say_hello(request):
    x = 1
    y = 2
    return render(request,"hello.html",{"name":"Mosh"})
