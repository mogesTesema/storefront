from rest_framework import serializers
from decimal import Decimal
from .models import Product,Collection,Review,Cart,CartItem






class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id','title','products_count']
    products_count = serializers.IntegerField(read_only=True)

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)









class ProductSerializer(serializers.ModelSerializer):


    class Meta:
        model = Product
        fields = ['id','title','unit_price','price_with_tax','collection','inventory']

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calcuate_tax')
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset= Collection.objects.all(),
    #     view_name = 'collection-detail'
    # )

    def calcuate_tax(self,product: Product):
        result = product.unit_price * Decimal(1.1)
        return result.quantize(Decimal('0.01'))
    

    
    """
    the save method call the following methods depends on the state of serializer
    """
    # def create(self,validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()

    #     return product
    
    # def update(self,instance,validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()

    """
    we can override build in validation to add custom validation logic in our serialize object.
    """
 
    # def validate(self,data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError("password don't match with confirmation password")
    #     return data


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['id','created_at','name','description'] 
    
    def create(self,validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)



class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    def get_total_price(self,cart_item):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,cart):
        item_prices = [item.quantity * item.product.unit_price for item in cart.items.all()]
        return sum(item_prices)
        ...
    class Meta:
        model = Cart
        fields = ['id','items','total_price']



class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID found.')
        return value

    def save(self,**kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id,**self.validated_data)
        return self.instance
    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = CartItem
        fields = ['quantity']