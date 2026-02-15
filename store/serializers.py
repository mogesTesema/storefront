from rest_framework import serializers
from decimal import Decimal
from .models import Product,Collection






class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id','title']

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
    