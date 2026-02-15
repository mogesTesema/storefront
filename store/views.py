from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin 
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSerializer
# Create your views here.


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()[:15]
    serializer_class = ProductSerializer
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()[:15]

    # def get_serializer_class(self):
    #     return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    

    # def get(self,request): 
    #     queryset = Product.objects.select_related('collection').all()[:15]
    #     serializer = ProductSerializer(queryset,many=True,context={'request': request})
    #     return Response(serializer.data)
    
    # def post(self,request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)
     
    
 


# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()[:15]
#         serializer = ProductSerializer(queryset,many=True,context={'request': request})
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
     
 
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get_object(self,id):
    #     return get_object_or_404(Product,pk=id)

    # def get(self,request,id):
    #     product = self.get_object(id)
    #     serializer = ProductSerializer(product,context={'request': request})
    #     return Response(serializer.data)
    
    # def put(self,request,id):
    #     product = self.get_object(id)
    #     serializer = ProductSerializer(product, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def delete(self,request,pk):

        product = get_object_or_404(Product,pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error':'product can not be deleted because it is associated with orderitem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT) 

   


# @api_view(["GET","PUT","DELETE"])
# def product_detail(request,id:int): 

#     product = get_object_or_404(Product,pk=id)  #Product.objects.get(pk=id)
#     if request.method == "GET":
#         serializer = ProductSerializer(product,context={'request': request})
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
#     elif request.method == "DELETE":
#         if product.orderitems.count() > 0:
#             return Response({'error':'product can not be deleted because it is associated with orderitem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

#         product.delete()

#         return Response(status=status.HTTP_204_NO_CONTENT) 



class CollectionList(ListCreateAPIView):
    """
    GenericeView that handles behaviors automatically by leveraging mixins and genericveiws database layer and APIViews http method handling capability.
    """
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer
    
    """
    APIView that handle http methods, define them and add premision and authentication over orginal parent view class.
    """
    # def get(self,request):
    #     collection = Collection.objects.annotate(products_count=Count('product')).all()
    #     serializer = CollectionSerializer(collection,many=True)
    #     return Response(serializer.data)
    
    # def post(self,request):
    #     serializer = CollectionSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data,status=201)


"""
functional view that you manually check methods and despatch based on the method.
"""



# @api_view(["GET","POST"])
# def collection_list(request):
#     if request.method == "GET":
#         collection = Collection.objects.annotate(products_count=Count('product')).all()
#         serializer = CollectionSerializer(collection,many=True)
#         return Response(serializer.data)
#     elif request.method== "POST":
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data,status=201)


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection
    serializer_class = CollectionSerializer

    # def get(self,request,pk):
    #     collection = get_object_or_404(Collection,pk=pk) 
    #     serializer = CollectionSerializer(collection)
    #     return Response(serializer.data)
    
    # def put(self,request,pk):
    #     collection = get_object_or_404(Collection,pk=pk) 
    #     serializer = CollectionSerializer(collection,data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data,status=201)
    
    # def delete(self,request,pk):
    #     collection = get_object_or_404(Collection,pk=pk) 
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(["GET","PUT","DELETE"])
# def collection_detail(request,pk):
#     collection = get_object_or_404(Collection,pk=pk) #Collection.objects.get(pk=pk)
#     if request.method == "GET":
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = CollectionSerializer(collection,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=201)
#     elif request.method == "DELETE":
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

