from typing import NoReturn
from django.db import connections, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from django.http import response
from django.shortcuts import render
from store.models import Collection, Customer, Product, OrderItem , Order

# Create your views here.



def say_hello(request):
    try:
        productInLine = OrderItem.objects.order_by('product_id').values('product_id').distinct()
        product = Product.objects.prefetch_related(
            'promotions').select_related('collections').all().filter(id__in=productInLine)
        connections.close_all()
        return render(request,'hello.html', {'products': list(product)})
    except ObjectDoesNotExist as odnex:
        return render(request,'hello.html',{'odnex':odnex})

def customer(request):
    try:
       querySet =  Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-place_at')[:5]
       queryTotalCustOrder = Customer.objects.annotate(orders_count=Count('order')).filter(orders_count__gt=0);
       connections.close_all()
       return render(request,'customer.html', {'orders': list(querySet), 'totalOrders': list(queryTotalCustOrder)})
    except ObjectDoesNotExist as odnex:
        return render(request,'customer.html',{'odnex':odnex})
@transaction.atomic()
def loadData(request):
    querySet = Collection.objects.values('title').filter(title = "Video Games")
    data = list(querySet)
    print(data)
    if (data == None):
          return response.HttpResponse(" 400 - Can't load data", content_type='text/plain' , status=400) 
    else:
        # --- Create
        collection = Collection()
        collection.title = 'Video Games'
        collection.featured_products = Product(pk=1)
        collection.save()
        connections.close_all()
        # --- Update
        # collection = Collection.objects.get(pk=1)
        # collection.featured_products = None
        # collection.save()
        # --- Delete
        # collection = Collection(pk=1)
        # collection.delete()
    return response.HttpResponse("data loaded")
