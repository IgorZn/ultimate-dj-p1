import datetime

from django.shortcuts import render
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db import transaction
from django.db.models.aggregates import Count, Max, Sum, Avg, Min

from store.models import Customer, Product, Collection, Order, OrderItem
from tags.models import TaggedItem

# Create your views here.


def say_hello(request):
    customers = None
    # products = Product.objects.all().filter(
    #     Q(inventory__gt=20) & Q(unit_price__lt=20)
    # ).order_by('unit_price')
    #
    # products = Product.objects.all().filter(
    #     inventory=F('collections_id')
    # ).order_by('unit_price')
    #
    # products = Product.objects.all()[5:10]
    #
    # products = Product.objects.values('id', 'title', 'collections__title')[:10]
    # products = Product.objects.values_list('id', 'title', 'collections__title')[:10]
    # products = Product.objects.filter(pk=F('collections__id'))
    # products = Product.objects.all().order_by('-unit_price', 'collections_id').reverse().first()
    # products = Product.objects.earliest('-unit_price', 'collections_id')
    # products = Product.objects.latest('-unit_price', 'collections_id')
    # products = Product.objects.all()[:5]
    # products = Product.objects.values('id', 'title', 'collections__title')[:5]
    # products = Product.objects.values_list('id', 'title', 'collections__title')[:5]
    products = Product.objects.only('id', 'title', 'collections__title')[:5]
    products = Product.objects.defer('title')[:5]   # всё, кроме  'title'

    # select_related -- ускоряет запрос, за счет прямой инструкции к связанной таблице, а не ч/з
    # доп вызов уже в самом шаблоне, что провоцирует кучу подзапросов уже при выводе
    products = Product.objects.select_related('collections').all()

    # для ManyToMany
    products = Product.objects.prefetch_related('promotions').all()

    # для ManyToMany + related
    products = Product.objects\
        .prefetch_related('promotions')\
        .select_related('collections')\
        .order_by('unit_price')\
        .all().reverse()[:5]

    # Aggregate, Count, Max
    products = Product.objects.aggregate(count=Count('unit_price'))
    products = Product.objects.aggregate(
        count=Count('unit_price'),
        min_goo=Min('unit_price'),
        max_price=Max('unit_price'),
        sum=Sum('unit_price')
    )

    queryset = Customer.objects.annotate(is_new_old=Value(True))
    queryset = Customer.objects.annotate(new_id=F('id') * 2)

    # call DB function CONCAT
    queryset = Customer.objects.annotate(
        full_name=Func(
            F('first_name'), Value(' '), F('last_name'), function='CONCAT'))

    # queryset = Customer.objects.annotate(
    #     full_name=Concat('first_name', Value(' '), 'last_name'))

    # Grouping
    queryset = Customer.objects.annotate(
        order_count=Count('order'))

    # ExpressionWrapper
    discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    queryset = Product.objects.annotate(
        discounted_price=discounted_price)

    # Custom Object manager
    queryset = TaggedItem.objects.get_tags_for(Product, 1)

    # Creating object
    # collections = Collection()
    # collections.title = 'Video game'
    # collections.featured_product = Product(pk=101)
    # collections.save()
    # collections.id

    # Creating object, short
    collections = Collection.objects.create(
        pk=Collection.objects.aggregate(count=Count('id'))['count'] + 1,
        title='a',
        featured_product=Product(pk=1)
    )
    collections.id

    # Update objects
    obj = Collection.objects.get(pk=101)
    setattr(obj, 'title', 'oooooooooooo')
    obj.save()

    # Delete objects
    # obj = Collection.objects.filter(pk=100)
    # obj.delete()
    #
    # obj = Collection.objects.filter(id__gte=101)
    # obj.delete()

    # # Transactions
    # from django.db import transaction
    # order = Order()
    # order.customer_id = 101
    # order.save()
    #
    # item = OrderItem()
    # item.order = order
    # item.product_id = 33
    # item.quantity = 12
    # item.unit_price = 41.33
    # item.save()


    context = {
        'name': 'Igor',
        'customers': customers,
        'products': products,
        'queryset': queryset
    }
    return render(request, 'hello.html', context)


def say_transaction(request):
    with transaction.atomic():
        # Transactions
        new_id_order = Order.objects.count() + 1
        tm = datetime.timedelta(weeks=3)
        delta = datetime.datetime.now() + tm
        placed_at = delta.strftime('%Y-%m-%d')

        order = Order.objects.create(
            pk=new_id_order,
            customer_id=101,
            placed_at=placed_at
        )

        # order = Order(pk=new_id_order)
        # order.customer_id = 101
        # order.placed_at = delta.strftime('%Y-%m-%d')
        # order.save()

        new_order_item_id = OrderItem.objects.count() + 1
        OrderItem.objects.create(
            pk=new_order_item_id,
            order=order,
            product_id=33,
            quantity=12,
            unit_price=41.33
        )

        # item = OrderItem(pk=new_order_item_id)
        # item.order = order
        # item.product_id = 33
        # item.quantity = 12
        # item.unit_price = 41.33
        # item.save()

    context = {
        'name': 'Igor',
    }
    return render(request, 'hello.html', context)
