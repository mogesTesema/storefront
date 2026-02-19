from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser,DjangoModelPermissions
from rest_framework.decorators import api_view,action
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
)
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Product, Collection, OrderItem, Review, Cart,CartItem,Customer
from .filters import ProductFilter
from .serializers import (
    ProductSerializer,
    CollectionSerializer,
    ReviewSerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    CustomerSerializer
)
from .permissions import IsAdminOrReadOnly,FullDjangoModelPermissions,ViewCustomerHistoryPermission
from .pagination import DefaultPagination
# Create your views here.










class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title", "description", "collection__title"]
    ordering_fields = ["unit_price", "last_update"]
    # filterset_fields = ['collection_id','unit_price']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id',None)
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    def destory(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "product can not be deleted because it is associated with orderitem"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().destory(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("product")).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs["pk"])
        if collection.product_set.count() > 0:
            return Response(
                {
                    "error": "collection cannot be deleted since it is associated with products."
                }
            )

        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class CartViewSet(
    CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer





class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        if self.request.method =="PATCH":
            return UpdateCartItemSerializer
    
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

    def get_queryset(self): 
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')
    




class CustomerViewSet(ModelViewSet):
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'user_id':self.request.user.id
        })
        return context

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return [IsAuthenticated()]
    @action(detail=True,permission_classes=[ViewCustomerHistoryPermission])
    def history(self,request,pk):
        customer = get_object_or_404(Customer,user_id=pk)
        if customer:
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        return Response("customer don't exist")



    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self,request):
        (customer,created )= Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
                
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)







    # def delete(self,request,pk):
    #     product = get_object_or_404(Product,pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({'error':'product can not be deleted because it is associated with orderitem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # class ProductList(ListCreateAPIView):
    #     queryset = Product.objects.all()[:15]
    #     serializer_class = ProductSerializer
    #     # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()[:15]

    # def get_serializer_class(self):
    #     return ProductSerializer

    # def get_serializer_context(self):
    #     return {'request': self.request}

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

    # class ProductDetail(RetrieveUpdateDestroyAPIView):
    #     queryset = Product.objects.all()
    #     serializer_class = ProductSerializer

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

    # def delete(self,request,pk):

    #     product = get_object_or_404(Product,pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({'error':'product can not be deleted because it is associated with orderitem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    #     product.delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)

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

    # def delete(self,request,pk):
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # class CollectionList(ListCreateAPIView):
    """
    GenericeView that handles behaviors automatically by leveraging mixins and genericveiws database layer and APIViews http method handling capability.
    """
    # queryset = Collection.objects.annotate(products_count=Count('product')).all()
    # serializer_class = CollectionSerializer

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


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('product')
#     )
#     serializer_class = CollectionSerializer

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
#     if collection.product_set.count() > 0:
#         return Response({"error":"collection cannot be deleted since it is associated with products."})
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
