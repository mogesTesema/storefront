from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSerializer
# Create your views here.



@api_view(['Get','POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()[:15]
        serializer = ProductSerializer(queryset,many=True,context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
     
    else:
        raise()


@api_view(["GET"])
def product_detail(request,id:int):
    product = get_object_or_404(Product,pk=id)  #Product.objects.get(pk=id)
    serializer = ProductSerializer(product,context={'request': request})
    return Response(serializer.data)
  


@api_view()
def collection_detail(request,pk):
    collection = Collection.objects.get(pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)
