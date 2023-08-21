from django.urls import path

from .views import say_hello, say_transaction

urlpatterns = [
    path('', say_hello, name='say_hello'),
    path('tr/', say_transaction, name='say_transaction')
]
