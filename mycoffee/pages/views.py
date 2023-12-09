from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from products.models import Product
def index(requset):


    context={
        'products':Product.objects.all()

    }
    return render(requset,'pages/index.html',context)

def about(requset):
    return render(requset,'pages/about.html')
def coffee(requset):
    return render(requset,'pages/coffee.html')