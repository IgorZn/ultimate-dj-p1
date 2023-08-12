from django.shortcuts import render
from django.db.models import Q, F

from store.models import Customer, Product

# Create your views here.


def say_hello(request):
    customers = None
    products = Product.objects.all().filter(
        Q(inventory__gt=20) & Q(unit_price__lt=20)
    ).order_by('unit_price')

    products = Product.objects.all().filter(
        inventory=F('collections_id')
    ).order_by('unit_price')

    products = Product.objects.all()[5:10]

    products = Product.objects.values('id', 'title', 'collections__title')[:10]
    products = Product.objects.values_list('id', 'title', 'collections__title')[:10]
    products = Product.objects.filter(pk=F('collections__id'))
    products = Product.objects.all().order_by('-unit_price', 'collections_id').reverse().first()
    products = Product.objects.earliest('-unit_price', 'collections_id')
    products = Product.objects.latest('-unit_price', 'collections_id')

    context = {
        'name': 'Igor',
        'customers': customers,
        'products': products
    }
    return render(request, 'hello.html', context)
