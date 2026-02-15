from rest_framework import serializers
from decimal import Decimal
from .models import Product,Collection






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