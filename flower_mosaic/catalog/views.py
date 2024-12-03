from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Product


def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/catalog.html', {'products': products})


@require_POST
def add_to_cart(request, product_id):

   cart = request.session.get('cart', {})
   if str(product_id) in cart:
       cart[str(product_id)] += 1
   else:
       cart[str(product_id)] = 1

   request.session['cart'] = cart

   return redirect('catalog')
