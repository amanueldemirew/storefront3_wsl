from django.shortcuts import render
from .task import notify_customer


def say_hello(request):
    notify_customer.delay('hello')
    return render(request, 'hello.html', {'name': 'Mosh'})
