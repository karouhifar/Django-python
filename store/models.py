from django.db import models


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
#-----------------------------------------------------------
class Collection(models.Model):
    title = models.CharField(max_length=200)
    # '+' sign refers to not to create reverse relationship in Product model
    featured_products = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')    
#-----------------------------------------------------------
class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    # 9999.99
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory= models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collections = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
#-----------------------------------------------------------
class Customer(models.Model): 
    MEMBERSHIP_CHOICES = [
        ('B','bronze'),
        ('S','Silver'),
        ('G','Gold')
    ]
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200)
    birth_date = models.DateTimeField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default= 'B')

#-----------------------------------------------------------
class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('P','Pending'),
        ('C','Complete'),
        ('F','Failed'),
    ]
    place_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default= 'P')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
#-----------------------------------------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
#-----------------------------------------------------------
# One-to-One Relationship Address and Customer
# class Address(models.Model):
#     street = models.CharField(max_length=200)
#     city = models.CharField(max_length=200)
#     customer = models.OneToOneField(Customer,on_delete=models.CASCADE, primary_key=True)
# One-to-Many Relationship Address and Customer
class Address(models.Model):
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)

# Many-to-Many Relationship Address and Customer
# class Address3(models.Model):
#     street = models.CharField(max_length=200)
#     city = models.CharField(max_length=200)
#     customer = models.ManyToManyField(Customer)
#-----------------------------------------------------------
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

#-----------------------------------------------------------
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


        