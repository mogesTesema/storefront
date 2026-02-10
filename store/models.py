from django.db import models

# Create your models here.


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()



class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey("Product",on_delete=models.SET_NULL,null=True,related_name="+")

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["title"]





class Product(models.Model): 
    # sku = models.CharField(max_length=10,primary_key=True) # django automatically create id field for every class models
    title = models.CharField(max_length=254)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(to=Collection,on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["title"]


class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_SILIVER = "S"
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,"Bronze"),
        (MEMBERSHIP_GOLD,"Gold"),
        (MEMBERSHIP_SILIVER,"Siliver")
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone =  models.CharField(max_length=20)
    birth_date = models.DateField(null=False)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return  f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name','last_name']






class Order(models.Model):
    PAYMENT_STATUS_PANDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PANDING,"panding"),
        (PAYMENT_STATUS_COMPLETE,"complete"),
        (PAYMENT_STATUS_FAILED,"failed")
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_STATUS_PANDING)
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE )


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_length=6,decimal_places=2,max_digits=5)


class Address(models.Model): 
    street = models.CharField(max_length=255)   
    zip = models.CharField(max_length=15)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)



class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)




class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
