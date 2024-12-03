from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/catalog.html', {'products': products})


def cart(request):
    return render(request, 'catalog/cart.html')
