from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSerializer
# Create your views here.



@api_view(['GET','POST'])
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


@api_view(["GET","PUT","DELETE"])
def product_detail(request,id:int): 

    product = get_object_or_404(Product,pk=id)  #Product.objects.get(pk=id)
    if request.method == "GET":
        serializer = ProductSerializer(product,context={'request': request})
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        if product.orderitems.count() > 0:
            return Response({'error':'product can not be deleted because it is associated with orderitem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT) 

  

@api_view(["GET","POST"])
def collection_list(request):
    if request.method == "GET":
        collection = Collection.objects.annotate(products_count=Count('product')).all()
        serializer = CollectionSerializer(collection,many=True)
        return Response(serializer.data)
    elif request.method== "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=201)


@api_view(["GET","PUT","DELETE"])
def collection_detail(request,pk):
    collection = get_object_or_404(Collection,pk=pk) #Collection.objects.get(pk=pk)
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=201)
    elif request.method == "DELETE":
        collection.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
