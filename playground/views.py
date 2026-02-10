from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F,Value,Func,ExpressionWrapper,DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count,Max,Min,Avg,Sum
from django.db import transaction,connection
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from store.models import Product, OrderItem, Order,Customer,Collection
from tags.models import TaggedItem




# it is request-handle, action, the name view is so confusing.
def say_hello(request):
    # query_set1 = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=10))
    # query_set2 = Product.objects.filter(inventory__gt=F('unit_price'))
    # query_set3 = Product.objects.order_by("-unit_price","title").reverse()
    # query_set4 = Product.objects.filter(collection__id=3).filter(Q(inventory__gte=10)& Q(unit_price__gte=20)).order_by("unit_price").reverse()[:20]
    # query_set5 = Product.objects.values_list("unit_price","title","inventory","collection__title").order_by("unit_price").reverse()[:20]
    # query_set6 = OrderItem.objects.values("product__title","product__inventory","product__unit_price").order_by("product__title")
    # query_set = Product.objects.earliest("unit_price")
    # query_set = product.objects.least("unit_price")
    # pordered_product_set = OrderItem.objects.values('product__id').distinct()
    # query_set = Product.objects.filter(id__in=pordered_product_set).order_by("title")
    # query_set = Product.objects.defer("id","title")

    # select_related when the object has one instance of desired object,one-to-many relationship, uses on join query
    # prefetch_related when the object can have many instance of desired object, many-to-many relationship, uses two quey
    # query_set = Product.objects.select_related("collection__title").all()
    # query_set = Product.objects.prefetch_related("promotions").select_related("collection").all()

    # result = Product.objects.filter(collection__id=3).aggregate(count=Count('id'),min_price=Min('unit_price'))
    # query_set = Order.objects.select_related("customer").prefetch_related("orderitem_set__product").order_by('-placed_at')[:5]
    # query_set = Customer.objects.annotate(is_new=Value(True),
    #                                       new_id=F('id')+1,
    #                                       full_name=Func(F('first_name'),Value(' '),F('last_name'),function="CONCAT"),
    #                                       )
    
    # query_set = Customer.objects.annotate(full_name=Concat('first_name',Value(' '),'last_name')
    #          
    # 
    #                              )
    # discounted_price =ExpressionWrapper(F('unit_price')*0.8,output_field=DecimalField())
    # query_set = Product.objects.annotate(discount_price=discounted_price)

   
    # query_set = Customer.objects.annotate(orders=Count('order'))

    # query_set = TaggedItem.objects.get_tags_for(Product,3)
    # products = list(query_set)
    # total_products = len(products) 

    collection = Collection(pk=112)
    # collection.title = "laptop accessaries"
    # collection.featured_product = Product(pk=212)
    # collection.featured_product_id = 2
    # collection.save()
    Collection.objects.filter(pk=112).update(featured_product=32)
    Collection.objects.filter(pk=111).delete()
    

    query_set = Collection.objects.create(title="aninamtion game",featured_product_id=1)
    products = "list(query_set)"

    # Transaction
    with transaction.atomic():
        order = Order()
        order.customer_id =3
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 4
        item.quantity = 3
        item.unit_price = 24
    raw_data = Customer.objects.raw("SELECT * FROM store_customer where id>90")
    with connection.cursor() as cursor:
        cursor.execute("insert into store_customer values('2222','moges','tesema','mogess@gmail.com','223-2323','1980-01-01','G')")
    return render(request,"hello.html",{"name":"Moges","products":products,"tags":list(raw_data)})
 